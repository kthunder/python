let currentEngine = engines.myEngine()
let runningEngines = engines.all()
let currentSource = currentEngine.getSource() + ''
if (runningEngines.length > 1) {
    runningEngines.forEach(compareEngine => {
        let compareSource = compareEngine.getSource() + ''
        if (currentEngine.id !== compareEngine.id && compareSource === currentSource) {
            // 强制关闭同名的脚本
            compareEngine.forceStop()
        }
    })
}

if (!requestScreenCapture()) {
    toastLog('请求截图权限失败')
    exit()
}
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
let x = 0
let y = 0

window.canvas.on('draw', function (canvas) {
    // 清空内容
    canvas.drawColor(0xFFFFFF, android.graphics.PorterDuff.Mode.CLEAR)
    // paint.setARGB(0xFF, 0xFF, 0, 0)
    canvas.drawCircle(x, y, 30, paint)
})

while (1) {
    sleep(1000)
    x += 100
    y += 100
    x %= 800
    y %= 800
}

setInterval(() => { }, 10000)
events.on('exit', () => {
    // 撤销监听
    window.canvas.removeAllListeners()
})

