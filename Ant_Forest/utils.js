var thread1 = threads.start(function () {
    let count = 0;
    while (1) {
        console.log(count++);
        sleep(1000);
    }
});

