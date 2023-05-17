let currentEngine = engines.myEngine()
let currentSource = engines.myEngine().getSource() + ''
engines.all().forEach(engine => {
    let compareSource = engine.getSource() + ''
    if (currentEngine.id != engine.id && compareSource === currentSource) {
        // 强制关闭同名的脚本
        engine.forceStop()
    }
})

function main() {
    auto.waitFor()
    threads.start(function () {
        text("立即开始").findOne(1000).click()
    });
    res = requestScreenCapture()
    app.startActivity({
        action: 'VIEW',
        data: 'alipays://platformapi/startapp?appId=60000002',
        packageName: 'com.eg.android.AlipayGphone'
    })
    textContains("g").waitFor();
    sleep(1000)
    toastLog("开始收能量")
    energyHarvester()
    sleep(1000)
    toastLog("开始能量雨")
    energyRain()
    exit()
}

function energyHarvester() {
    do {
        textContains("g").findOne(2000);
        sleep(1000)
        if (text('沙柳皮肤').exists() || text('山杏皮肤').exists()) {
            // toast('沙柳和能量无法识别，下一个')
            click(537, 1990)
            findEnergy()
            textContains("g").findOne(2000);
            sleep(1000)
        }
        while (clickEnergy()) {
            sleep(200)
        }
    } while (findEnergy());
}

function findEnergy() {
    let point = findColor(captureScreen(), "#FF802C", {
        region: [830, 1530, 200, 90],
    });
    toastLog(point ? "下一棵树" : "无");
    sleep(random(0.5, 1))
    return point ? clickP(point.x, point.y) : false
}

function energyRain() {
    // 判断是否收完了
    if (text("天天能量雨已完成").exists()) {
        toastLog("收集能量结束");
        cilckCenter(text("返回我的森林").findOne());
    }

    for (let index = 0; index < 3; index++) {
        if (text("去收取").findOne(1000)) {
            cilckCenter(text("去收取").findOne(1000));
        }
        else if (text("去赠送").findOne(1000)) {
            cilckCenter(text("去赠送").findOne(1000));
            sleep(500)
            cilckCenter(text("送TA机会").findOne(1000));
        }
        else {
            return false
        }

        sleep(500)

        if (text("立即开启").exists()) {
            cilckCenter(text("立即开启").findOne());
            let BeginTime = new Date().getTime()
            let ElapsedTime = 0
            while (ElapsedTime < 15000) {
                clickEnergy()
                ElapsedTime = new Date().getTime() - BeginTime
            }
        }
    }
}

function clickEnergy() {
    point = findColor(captureScreen(), "#DEFF00", {
        region: [150, 600, 800, 150],
    })
    return point ? clickP(point.x, point.y) : false
}

function clickP(x, y) {
    return press(x, y, 1);
}

// 点击控件中间
function cilckCenter(uiObject) {
    if (uiObject) {
        clickP(uiObject.bounds().centerX(), uiObject.bounds().centerY());
        sleep(300);
    }
}

main()