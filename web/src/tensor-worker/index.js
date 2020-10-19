const worker = new Worker('./MLWorker.js', {type: 'module'});

const send = message => worker.postMessage({
    message
})

export default {
    worker,
    send
}