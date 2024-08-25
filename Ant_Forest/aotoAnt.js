let currentEngine = engines.myEngine()
let currentSource = engines.myEngine().getSource() + ''
engines.all().forEach(engine => {
    let compareSource = engine.getSource() + ''
    if (currentEngine.id != engine.id && compareSource === currentSource) {
        // 强制关闭同名的脚本
        engine.forceStop()
    }
})

/************************************UI****************************************/
if (!floaty.checkPermission()) {
    toastLog('无悬浮窗权限')
    floaty.requestPermission()
    if (!floaty.checkPermission())
        exit()
}
// 绘制识别结果
let window = floaty.rawWindow(
    <canvas id="canvas" layout_weight="1" />
);
// 设置悬浮窗位置
ui.post(() => {
    window.setPosition(0, -120)
    window.setSize(device.width, device.height)
    window.setTouchable(false)
})


let Typeface = android.graphics.Typeface
let paint = new Paint()
paint.setStrokeWidth(3)
paint.setStyle(Paint.Style.STROKE)
paint.setTypeface(Typeface.DEFAULT_BOLD)
paint.setARGB(0xFF, 0xFF, 0, 0)

let cx = 0
let cy = 0

window.canvas.on('draw', function (canvas) {
    // 清空内容
    canvas.drawColor(0xFFFFFF, android.graphics.PorterDuff.Mode.CLEAR)
    canvas.drawCircle(cx, cy, 30, paint)
})

setInterval(() => { }, 10000)
events.on('exit', () => {
    // 撤销监听
    window.canvas.removeAllListeners()
})
/************************************ant****************************************/
function OcrClick(text) {
    img = captureScreen()
    // let start = new Date()
    result = paddle.ocr(img);
    // result = paddle.ocr(img, region = [0, device.height/2, device.width, device.height/3]);
    // toastLog('耗时' + (new Date() - start) + 'ms')
    // log(result);
    let btn = result.find(e => { 
        if (e.text.includes(text) && (e.bounds.centerY()>device.height/2)) {
            toastLog(e.text)
            toastLog(e.bounds.centerX())
        }
        
        return e.text.includes(text) && (e.bounds.centerY()>device.height/2)
    })
    // toastLog(btn.text)
    // if (btn) click(btn.bounds)
    if (btn) cilckCenter(btn)
    img.recycle()

    return btn ? true : false
}

function clickP(x, y) {
    cx = x
    cy = y
    return press(x, y, 1);
}

function clickEnergy() {
    // toastLog("开始查找能量球")
    point = findColor(captureScreen(), "#DEFF00", {
        region: [200, 700, 1000, 400],
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

function findEnergy() {
    return OcrClick("找能量")
}

function collectEnergy() {
    return OcrClick("键收")
}

// main function
function main() {
    auto.waitFor()
    threads.start(function () {
        sleep(300)
        click(1200, 2040)
    })
    requestScreenCapture()

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
        if (text('找能量共获得').exists()) {
            toastLog("找能量结束")
        } else {
            toastLog("开始收集能量")
            sleep(1000)
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
        if (text("去收取").exists()) {
            text("去收取").findOne(1000).click()
        }
        else if (text("去赠送").exists()) {
            text("去赠送").findOne(1000).click()
            sleep(500)
            text("送TA机会").findOne(1000).click()
        }
        else {
            return false
        }

        sleep(1500)

        if (text("立即开启").exists()) {
            text("立即开启").findOne().click()
            let BeginTime = new Date().getTime()
            let ElapsedTime = 0
            while (ElapsedTime < 17000) {
                // clickEnergy()
                sleep(15)
                clickP(200,1000)
                clickP(500,1000)
                clickP(750,1000)
                clickP(950,1000)
                clickP(1250,1000)
                ElapsedTime = new Date().getTime() - BeginTime
            }
        }
    }
}
main()