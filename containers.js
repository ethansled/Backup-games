const { Docker } = require("node-docker-api");
const { readdirSync } = require("fs");
const tar = require("tar-fs");
const path = require("path");
const { Http2ServerRequest } = require("http2");
const docker = new Docker({ socketPath: '/var/run/docker.sock' });

const promisifyStream = stream => new Promise((resolve, reject) => {
    stream.on('data', data => Logger.log(data.toString()))
    stream.on('end', resolve)
    stream.on('error', reject)
});

function getAppDirectoryList() {
    return readdirSync(path.resolve(__dirname, 'docker'), { withFileTypes: true })
        .filter(dirent => dirent.isDirectory())
        .map(dirent => dirent.name)
}

const Logger = {

    lines: [],

    log: (line) => {
        Logger.lines.push({
            timestamp: Date.now(),
            content: line
        })
    },

    read: () => { return Logger.lines.shift() },

    dump: async () => {
        Logger.lines.sort((a, b) => a.timestamp - b.timestamp)
        while (Logger.lines.length > 0) {
            let l = Logger.read();
            if (l) {
                console.log(`[ ${l.timestamp} ] : ${l.content}`)
            }
        }
    }

}

const ContainerManager = {
    containers: {},

    init: function () {
        docker.network.list().then(async (networks) => {
            if (!(networks.map((n) => n.data.Name).includes("pigbag"))) {
                await docker.network.create({
                    Name: "pigbag",
                    Attachable: true,
                })
            }
        })
            .then(() => docker.image.build(tar.pack('./docker'), {
                t: 'pygbag',
                nocache: false,
            }))
            .then(stream => promisifyStream(stream))
            .then(() => {
                Logger.log("Image initialized");
                // return docker.container.prune().then((c) => Logger.log(`Removed container ${c}`)).catch(() => { "Issue pruning containers" });
            })
            .then(async () => await ContainerManager.initContainers())
            .catch((r) => { Logger.log(`Build failed with error ${r}`) })
            .finally(() => Logger.dump());
    }(),

    initContainers: async function () {
        return ContainerManager.initProxy().then(async () => {
            for (let d of getAppDirectoryList()) {
                await ContainerManager.killContainer(d)
                Logger.log(`Starting ${d}`)
                await ContainerManager.initContainer(d)
                Logger.dump();
            }
        });
    },


    killContainer: async function (name) {
        Logger.log(`Attempting to stop container ${name}`);
        return docker.container.get(name).kill().then(async (c) => {
            Logger.log(`Waiting for ${name} to stop`)
            await c.wait();
            Logger.log(`Killed container ${name}`)
            return c.delete({ Force: true });
        }).catch((e) => Logger.log(`container ${name} does not exist/is not running`));
    },

    initContainer: async (appTarget) => {
        Logger.log(`Creating container ${appTarget}`);
        return docker.container.create(
            {
                Image: 'pygbag',
                name: appTarget,
                Cmd: ["/bin/bash", "-c", `/usr/local/bin/python -m pygbag --html --port 8080 ${appTarget}`],
                Hostname: appTarget,
                ExposedPorts: {
                    "8080/tcp": {}
                }
            })
            .then(container => container.start())
            .then(container => {
                Logger.log(`Connecting container ${container.id} to network`)
                docker.network.get("pigbag").connect(
                    { Container: container.id });
                return container;
            })
            .then((container) => {
                Logger.log(`started container ${container.id}`);
                return container.status();
            })
            .then(container => {
                setTimeout(() => {
                    ContainerManager.containers[container.data.Name] = container.data.NetworkSettings.IPAddress;
                }, 2000)
            })
            .catch((err) => Logger.log(`There was an error while starting container ${appTarget}: ${err}`));
    },

    initProxy: () => docker.image.build(tar.pack("./docker", { entries: ["pyproxy.conf", "nginx.Dockerfile"] }), {
            t: "pyproxy",
            nocache: true,
            dockerfile: "nginx.Dockerfile",
        })
            .then((s) => promisifyStream(s))
            .then(() => {
                Logger.log("starting pyproxy")
                return Logger.dump();
            })
        .then(() => docker.container.create({
            Image: "pyproxy",
            name: "pyproxy",
            HostConfig: {
                PortBindings: {
                    "8080/tcp": [
                        { "HostPort": "8080" }
                    ]
                }
            }
        }))
            .then((c) => c.start())
            .then((c) => docker.network.get("pigbag").connect({ Container: c.id }))
            .catch((r) => Logger.log("Failed to initialize pyproxy"))
            .finally(() => Logger.log(`initialized pyproxy`)),

    forwardRequest(appId, res) {
        
    }
}