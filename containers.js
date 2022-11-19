const { Docker } = require('node-docker-api');
const tar = require('tar-fs');

const docker = new Docker({ socketPath: '/var/run/docker.sock' });

const promisifyStream = stream => new Promise((resolve, reject) => {
  stream.on('data', data => console.log(data.toString()))
  stream.on('end', resolve)
  stream.on('error', reject)
});

console.log("building container");
docker.image.build(tar.pack('.', { entries: ["games", "Dockerfile", "nginx.conf", "build.sh"] }), {
    t: 'webserver',
})
    .then(stream => promisifyStream(stream))
    .then(() => docker.container.create({
        Image: 'webserver',
        name: 'webserver',
        HostConfig: {
            PortBindings: {
                "8080/tcp": [
                    {
                        HostIp: "0.0.0.0",
                        HostPort: "8080"
                    }
                ]
            }
        }
    }))
    .then((c) => c.start())
    .then((c) => c.logs({ stdout: true, stderr: true }))
    .then(stream => promisifyStream(stream))
    .catch((r) => console.log(`skipping container init due to ${r}`));



class ContainerManager {
    static getContainer() {
        return docker.container.get("webserver")
    }
}