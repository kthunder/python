let currentEngine = engines.myEngine()
let currentSource = engines.myEngine().getSource() + ''
engines.all().forEach(engine => {
    let compareSource = engine.getSource() + ''
    if (currentEngine.id != engine.id && compareSource === currentSource) {
        // 强制关闭同名的脚本
        engine.forceStop()
    }
})

var window = floaty.rawWindow(
    <frame>
        <text id="text" text="+" textColor="red" />
    </frame>
);

// tool functions
function displayP(x, y) {
    window.setPosition(x - 13, y - 27)
}

function clickP(x, y) {
    displayP(x, y)
    return press(x, y, 1);
}

function clickEnergy() {
    // toastLog("开始查找能量球")
    point = findColor(captureScreen(), "#DEFF00", {
        region: [150, 600, 800, 150],
    })

    return point ? clickP(point.x, point.y) : false
}

// 点击控件中间
function cilckCenter(uiObject) {

    if (uiObject) {
        if ("centerX" in uiObject.bounds) {
            clickP(uiObject.bounds.centerX(), uiObject.bounds.centerY());
        } else {
            clickP(uiObject.centerX(), uiObject.centerY());
        }

        sleep(300);
    }
}

function findButtonByOCR(text, region) {
    let button = null
    sleep(random(0.5, 1))
    // toastLog("查找" + text)
    if (arguments[1] === undefined) {
        button = ocr.detect().find(item => item.label.includes(text))
    } else {
        button = ocr.detect(region).find(item => item.label.includes(text))
    }

    // toastLog(button ? "存在" : "不存在")
    return button
}

function findEnergy() {
    button = findButtonByOCR("找能量", [800, 1500, 280, 200])
    cilckCenter(button)
    return button ? true : false
}

function collectEnergy() {
    button = findButtonByOCR("一键收")
    cilckCenter(button)
    return button ? true : false
}

// main function
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
    textContains("去保护").waitFor();
    sleep(2000)
    energyHarvester()
    sleep(2000)
    energyRain()
    exit()
}

function energyHarvester() {
    do {
        textContains("g").findOne(2000);
        sleep(1000)
        // if (text('沙柳皮肤').exists() || text('山杏皮肤').exists()) {
        //     // toast('沙柳和能量无法识别，下一个')
        //     click(537, 1990)
        //     findEnergy()
        //     textContains("g").findOne(2000);
        //     sleep(1000)
        // }
        if (text('找能量共获得').exists()) {
            toastLog("找能量结束")
        } else {
            toastLog("开始收集能量")
            while (collectEnergy());
            sleep(1000)
            while (clickEnergy());
            sleep(1000)
            toastLog("查看下一个人")
        }

    } while (findEnergy());
}


function energyRain() {
    // 判断是否收完了
    if (text("天天能量雨已完成").exists()) {
        toastLog("天天能量雨已完成");
        return
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

        sleep(1500)

        if (text("立即开启").exists()) {
            cilckCenter(text("立即开启").findOne());
            let BeginTime = new Date().getTime()
            let ElapsedTime = 0
            while (ElapsedTime < 15000) {
                clickEnergy()
                sleep(20)
                ElapsedTime = new Date().getTime() - BeginTime
            }
        }
    }
}


main()