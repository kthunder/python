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
// auto.waitFor()
// if (!requestScreenCapture()) {
//   toastLog('请求截图权限失败')
//   exit()
// }

// 获取状态栏高度
let offset = -getStatusBarHeightCompat()
console.log(offset);


let window = floaty.rawWindow(
    <canvas id="canvas" layout_weight="1" />
);

// 设置悬浮窗位置
ui.post(() => {
    // window.setPosition(0, 0)
    // window.setSize(device.width, device.height)
    window.setTouchable(false)
})

let Typeface = android.graphics.Typeface
let paint = new Paint()
paint.setTypeface(Typeface.DEFAULT_BOLD)
paint.setTextAlign(Paint.Align.LEFT)
paint.setAntiAlias(true)
paint.setStrokeJoin(Paint.Join.ROUND)
paint.setDither(true)
paint.setStrokeWidth(5)
paint.setStyle(Paint.Style.STROKE)
paint.setARGB(255, 0xFF, 0x00, 0x00)

// window.canvas.on('draw', function (canvas) {
//     canvas.drawColor(0xFFFFFF, android.graphics.PorterDuff.Mode.CLEAR)
//     drawX(800, 1800, canvas)
// })

function drawX(x, y, canvas) {
    canvas.drawLine(x, y - 50, x, y + 50, paint);
    canvas.drawLine(x - 50, y, x + 50, y, paint);
}

/**
 * 获取状态栏高度
 *
 * @returns
 */
function getStatusBarHeightCompat() {
    let result = 0
    let resId = context.getResources().getIdentifier("status_bar_height", "dimen", "android")
    if (resId > 0) {
        result = context.getResources().getDimensionPixelOffset(resId)
    }
    if (result <= 0) {
        result = context.getResources().getDimensionPixelOffset(R.dimen.dimen_25dp)
    }
    return result
}
