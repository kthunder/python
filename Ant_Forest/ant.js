main();
// 立即执行
function init() {
	//   

	// 请求无障碍
	auto.waitFor();
	//   threads.start(function () {
	//     let startBtn = textContains('立即开始').findOne(2000);
	//     sleep(500)
	//     if (startBtn) {
	//       startBtn.click()
	//       threads.currentThread().interrupt();
	//     }
	//   })
	// 请求截图权限
	if (!requestScreenCapture()) {
		console.log("请求截图失败");
		exit();
	}
}

function main() {
	// setScreenMetrics(1080, 2400);
	auto.waitFor();
	res = requestScreenCapture();
	console.log("请求截图权限", res);
	launchApp('支付宝');
	// 每个手机打开的速度不一样，等待1.5s
	sleep(1500);

	do {
		sleep(2000);
		while (energyHarvester())
			sleep(200);
	} while (findEnergy());
	energyRain()
	// if (textStartsWith('去收取').exists()) {
	// 	energyRain()
	// }
	
}


function energyHarvester() {
	// console.log(images.pixel(image, 891, 742))
	magic_number_energy = -6494453;

	var image, point;

	image = images.captureScreen()
	point = findColor(image, magic_number_energy, {
		region: [200, 550, 700, 300],
		threshold: 20,
	})
	if (point) {
		console.log("找到能量，坐标为(" + point.x + ", " + point.y + ")");
		click(point.x, point.y);
		return true
	}
	else {
		console.log("没找到能量")
		if (text('沙柳皮肤').exists() || text('山杏皮肤').exists()) {
			// toast('沙柳和能量无法识别，下一个')
			// delay(0.2)
			click(537, 1990)
			// findEnergy()
			return false
		}else
		{
			return false
		}
		
	}
	// if (textStartsWith('返回蚂蚁森林').exists()) {
	// 	toast('收完了');
	// 	home()
	// 	exit()
	// }



	// // 每个人的主页暂时定义是40次
	// if (errorCount > 20) {
	// 	// toast('点击超过40次了，该去下一个人了');
	// 	findEnergy()
	// 	break;
	// }

}

function findEnergy() {
	// console.log(images.pixel(image, 936, 1550))
	magic_number_next = -1731800;

	var image, point;
	
	image = images.captureScreen()

	point = findColor(image, magic_number_next, {
		region: [830, 1530, 200, 90],
		threshold: 40
	});

	if (point) {
		console.log("找到下一个按钮(" + point.x + ", " + point.y + ")");
		sleep(random(0.1, 0.3));
		click(point.x, point.y);
		return true
	}
	else {
		console.log("没找到下一个按钮")
		return false
	}
}

function energyRain() {
	// console.log(text('立即开启').findOnc(1000))
	// cilckCenter(text("立即开启").findOne());
}

function clickP(x, y) {
	//toastLog("click point(" + x + "," + y + ")");
	return press(x, y, 1);
}

// 点击控件中间
function cilckCenter(uiObject) {
	if (uiObject) {
		console.log(uiObject.bounds());
		clickP(uiObject.bounds().centerX(), uiObject.bounds().centerY());
		sleep(300);
	}
}