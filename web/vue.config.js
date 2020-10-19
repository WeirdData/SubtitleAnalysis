const WorkerPlugin = require('worker-plugin')
module.exports = {
    "transpileDependencies": [
        "vuetify"
    ],
    configureWebpack: {
        output: {
            globalObject: "this"
        },
        plugins: [
            new WorkerPlugin()
        ]
    }
}