let currentEngine = engines.myEngine()
let currentSource = engines.myEngine().getSource() + ''
engines.all().forEach(engine => {
    let compareSource = engine.getSource() + ''
    if (currentEngine.id != engine.id && compareSource === currentSource) {
        // 强制关闭同名的脚本
        engine.forceStop()
    }
})

// // 获取状态栏高度
// let offset = -getStatusBarHeightCompat()
// // console.log(offset);


// let window = floaty.rawWindow(
//     <canvas id="canvas" layout_weight="1" />
// );

// // 设置悬浮窗位置
// ui.post(() => {
//     window.setPosition(0, offset)
//     window.setSize(device.width, device.height)
//     window.setTouchable(false)
// })

// let Typeface = android.graphics.Typeface
// let paint = new Paint()
// paint.setTypeface(Typeface.DEFAULT_BOLD)
// paint.setTextAlign(Paint.Align.LEFT)
// paint.setAntiAlias(true)
// paint.setStrokeJoin(Paint.Join.ROUND)
// paint.setDither(true)
// paint.setStrokeWidth(5)
// paint.setStyle(Paint.Style.STROKE)
// paint.setARGB(255, 0xFF, 0x00, 0x00)

// window.canvas.on('draw', function (canvas) {
//     canvas.drawColor(0xFFFFFF, android.graphics.PorterDuff.Mode.CLEAR)
//     // drawX(500, 500,canvas)
//     // window.canvas.removeAllListeners()
//     drawX(800, 1800, canvas)
// })

// function drawX(x, y, canvas) {
//     canvas.drawLine(x, y - 50, x, y + 50, paint);
//     canvas.drawLine(x - 50, y, x + 50, y, paint);
// }

// /**
//  * 获取状态栏高度
//  *
//  * @returns
//  */
// function getStatusBarHeightCompat() {
//     let result = 0
//     let resId = context.getResources().getIdentifier("status_bar_height", "dimen", "android")
//     if (resId > 0) {
//         result = context.getResources().getDimensionPixelOffset(resId)
//     }
//     if (result <= 0) {
//         result = context.getResources().getDimensionPixelOffset(R.dimen.dimen_25dp)
//     }
//     return result
// }


function OcrClick(text) {
    img = captureScreen()
    // let start = new Date()
    result = paddle.ocr(img);
    // toastLog('耗时' + (new Date() - start) + 'ms')
    // log(result);
    let btn = result.find(e => e.text.includes(text))
    if (btn) click(btn.bounds)
    img.recycle()
    return btn ? true : false
}

function clickP(x, y) {
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
            while (ElapsedTime < 18000) {
                clickEnergy()
                sleep(20)
                ElapsedTime = new Date().getTime() - BeginTime
            }
        }
    }
}
main()