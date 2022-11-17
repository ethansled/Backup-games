const { Docker } = require('node-docker-api');
const tar = require('tar-fs');

const docker = new Docker({ socketPath: '/var/run/docker.sock' });

const promisifyStream = stream => new Promise((resolve, reject) => {
  stream.on('data', data => console.log(data.toString()))
  stream.on('end', resolve)
  stream.on('error', reject)
});

docker.image.build(tar.pack('.', { entries: ["games", "Dockerfile", "nginx.conf", "build.sh"] }), {
    t: 'webserver',
    nocache: true
}).then(stream => promisifyStream(stream))
.then(() => docker.container.create({
    Image: 'webserver',
    name: 'webserver',
    HostConfig: {
        PortBindings: {
            "8080:8080": {}
        }
    }
})).then((c) => c.start());