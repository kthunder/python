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
    //app.launchApp("支付宝")
    sleep(2000)
    toastLog("开始收能量")
    energyHarvester()
    sleep(1000)
    toastLog("开始能量雨")
    energyRain()
    exit()
}

function energyHarvester() {
    if (text('沙柳皮肤').exists() || text('山杏皮肤').exists()) {
        // toast('沙柳和能量无法识别，下一个')
        click(537, 1990)
        findEnergy()
    }
    do {
        sleep(2000)
        while (clickEnergy()) {
            sleep(100)
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

    for (let index = 0; index < 1; index++) {
        cilckCenter(text("去收取").findOne(1000));
        cilckCenter(text("去赠送").findOne(1000));
        cilckCenter(text("送TA机会").findOne(1000));
        if (text("立即开启").exists()) {
            cilckCenter(text("立即开启").findOne());
            var thread = threads.start(function () {
                while (1) {
                    clickEnergy()
                }
            });
            setTimeout(function () {
                threads.shutDownAll()
            }, 12000);
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