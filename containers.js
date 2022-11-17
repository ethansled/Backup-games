const { Docker } = require('node-docker-api');
const tar = require('tar-fs');

const docker = new Docker({ socketPath: '/var/run/docker.sock' });

const promisifyStream = stream => new Promise((resolve, reject) => {
  stream.on('data', data => console.log(data.toString()))
  stream.on('end', resolve)
  stream.on('error', reject)
});

try {
    console.log(`Using container ${docker.container.get("webserver").id}\n`);
} catch (error) {
    console.log(`Container not found, building...`)
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
        .then(stream => promisifyStream(stream));

}


class ContainerManager {
    static getContainer() {
        return docker.container.get("webserver")
    }
}