
program
    .version('0.0.1')
    .usage('[options] [ file ... ]\n\n' + '  Paste contents of file(s) or stdin to 0bin site.')
    .option('-u, --url [url]', 'URL of a 0bin site.')
    .option('-e, --expire [period]',
        'Expiration period - one of: 1_view, 1_day (default), 1_month, never.', '1_day')
    .option('-k, --entropy [bits]',
        'Encryption key entropy (and hence length) to use,'\
        + ' in bits, rounded up to multiple of 6 (default: 48).\n'\
        + '   That key will be processed by 1000 pbkdf2-sha256 iterations, not used as-is.', 48)
    .option('-c, --config [path]',
        'Path to zerobin configuration file (default: ~/.zerobinpasterc).\n'\
        + '   Should be json-file with the same keys as can be specified on the command line.\n'\
        + '   Example contents: {"url": "http://some-0bin.com"}', '~/.zerobinpasterc')
    .parse(process.argv);


[http, url, qs, fs, path] = ['http', 'url', 'querystring', 'fs', 'path'].map(require)


# Parse config file, if any
config = program.config.replace(/^~\/+/, '')
config = path.resolve(process.env.HOME, config)

try
    if fs.statSync(config).isFile()
        config = JSON.parse(fs.readFileSync(config))
        (program[k] = v) for own k, v of config


# Sanity checks and option processing
if not program.url
    console.error('ERROR: URL option must be specified.')
    process.exit(1)

if program.expire == '1_view'
    # "burn_after_reading" is too damn long for cli
    program.expire = 'burn_after_reading'

expire_opts = ['burn_after_reading', '1_day', '1_month', 'never']
if program.expire not in expire_opts
    console.error(
        "ERROR: --expire value (provided: '#{program.expire}')"\
        + ' must be one of: ' + expire_opts.join(', ') + "." )
    process.exit(1)

program.entropy = parseInt(program.entropy)


# Generated key will use base64 (6b per char) charset
# Key is not decoded for pbkdf2, so it's generated via base64 here just for convenience
generate_key = (entropy) ->
    entropy = Math.ceil(entropy / 6) * 6 # non-6-multiple produces same-length base64
    key = sjcl.bitArray.clamp(
        sjcl.random.randomWords(Math.ceil(entropy / 32), 0), entropy )
    return sjcl.codec.base64.fromBits(key, 0).replace(/\=+$/, '').replace(/\//, '-')


# Paste one dump and print URL, optionally prefixed with name
paste_file = (content, name) ->

    content = sjcl.codec.utf8String.toBits(content)
    content = sjcl.codec.base64.fromBits(content)
    # content = lzw.compress(content)

    key = generate_key(program.entropy)
    content = sjcl.encrypt(key, content)
    content = qs.stringify
        content: content
        expiration: program.expire

    # host.com -> http://host.com
    if not program.url.match(/^https?:\/\//)
        program.url = 'http://' + program.url.replace(/^\/+/, '')

    req_opts = url.parse(program.url)
    req_opts.method = 'POST'
    req_opts.headers =
        'Content-Type': 'application/x-www-form-urlencoded'
        'Content-Length': content.length

    req_url_base = req_opts.path
        .replace(/\/paste\/create\/?$/, '').replace(/\/+$/, '')
    req_opts.path = req_url_base + '/paste/create'

    req = http.request req_opts, (res) ->
        req_reply = ''
        res.setEncoding('utf8')
        res.on 'data', (chunk) -> req_reply += chunk
        res.on 'end', ->
            req_reply = JSON.parse(req_reply)
            if req_reply.status != 'ok'
                console.error("ERROR: failure posting #{name} - " + req_reply.message)
                return

            req_opts.pathname = req_url_base + '/paste/' + req_reply.paste
            req_opts.hash = key
            paste = url.format(req_opts)

            console.log(if name then "#{name} #{paste}" else paste)

    req.write(content)
    req.end()


# Seed sjcl prng from /dev/(u)random
do (bytes=64) ->
    for src in ['/dev/urandom', '/dev/random', null]
        break if not src or fs.existsSync(src)
    if not src
        console.error( 'ERROR: Failed to seed PRNG -'\
            + ' /dev/(u)random is unavailable, relying only on sjcl entropy sources' )
        return
    fd = fs.openSync(src, 'r')
    buff = new Buffer(bytes)
    fs.readSync(fd, buff, 0, bytes)
    fs.closeSync(fd)
    sjcl.random.addEntropy(
        (buff.readUInt32BE(n) for n in [0..bytes/4]), bytes * 8, src )


# Loop over file args or read stdin
if not program.args or not program.args.length
    process.stdin.resume()
    process.stdin.setEncoding('utf8')

    stdin_data = ''
    process.stdin.on 'data', (chunk) -> stdin_data += chunk
    process.stdin.on 'end', -> paste_file(stdin_data)

else
    for file in program.args
        paste_file( fs.readFileSync(file, 'utf8'),
            if program.args.length > 1 then path.basename(file) else null )
