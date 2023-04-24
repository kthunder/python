function main() {
	auto.waitFor()
	res = requestScreenCapture()
	toastLog("打开支付宝")
	launchApp('支付宝');
	sleep(1500)
	toastLog("打开蚂蚁森林")
	cilckCenter(text("蚂蚁森林").findOne());
	sleep(1500)
	toastLog("开始收能量")
	energyHarvester()
	sleep(1000)
	toastLog("开始能量雨")
	energyRain()
}

function energyHarvester() {
	toastLog("开始采集")
	if (text('沙柳皮肤').exists() || text('山杏皮肤').exists()) {
		// toast('沙柳和能量无法识别，下一个')
		click(537, 1990)
		findEnergy()
	}
	while (!clickEnergy()) {
		if (!findEnergy()) {
			break
		}
	}
	toastLog("采集完毕")
}

function findEnergy() {
	// toastLog(images.pixel(image, 936, 1550))
	magic_number_next = -1731800;
	let point = findColor(captureScreen(), magic_number_next, {
		region: [830, 1530, 200, 90],
		threshold: 30
	});
	toastLog(point ? "下一棵树" : "无");
	sleep(random(0.5, 1))
	return point ? clickP(point.x, point.y) : false
}

function energyRain() {
	if (text("去收取").exists()) {
		cilckCenter(text("去收取").findOne());
	}

	if (text("立即开启").exists()) {
		cilckCenter(text("立即开启").findOne());
		var thread = threads.start(function () {
			while (1) {
				clickEnergy()
			}
		});
		thread.join(8000)
	}

	if (text("天天能量雨已完成").exists()) {
		toastLog("收集能量结束");
		cilckCenter(text("返回我的森林").findOne());
	}
}

function clickEnergy() {
	// toastLog(images.pixel(image, 891, 742))
	magic_number_energy = -6494453;
	point = findColor(captureScreen(), magic_number_energy, {
		region: [150, 600, 800, 150],
		threshold: 15,
	})
	toastLog(point ? ("能量", point.x, point.y) : "没有能量了")
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