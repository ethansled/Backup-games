const { Docker } = require("node-docker-api")
const docker = new Docker({ socketPath: '/var/run/docker.sock' });
const tar = require('tar-fs')

const promisifyStream = stream => new Promise((resolve, reject) => {
  stream.on('data', data => console.log(data.toString()))
  stream.on('end', resolve)
  stream.on('error', reject)
});


class ContainerManager {

    static containers = {};
    static isImageBuilt = false;

    buildImage() {
        tarStream = tar.pack('./games');
        docker.image.build(tarStream, {
            t: 'gamebase',
            nocache: true,
        }).then(stream => promisifyStream(stream)).then(() => isImageBuilt = true);
    }
    
    static {
        buildImage();
    }

    initContainer(appTarget) {

        docker.container.create({
            Image: 'gamebase',
            name: appTarget,
            Cmd: ['/usr/local/bin/python', '-m', 'pygbag', appTarget]
        })
        .then(container => container.start())
        .then(container => containers[appTarget] = container);
    }

    forwardRequest(appId, res) {
        
    }
    
}

export default ContainerManager;