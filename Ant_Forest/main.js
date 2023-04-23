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

function main() {
	// 检查无障碍
	auto();

	app.launchApp("钉钉");
	// sleep(500)

	//if (!text("打卡").findOne()) {
		text("工作台").waitFor();
		cilckCenter(text("工作台").findOne());

		text("全员").waitFor();
		cilckCenter(text("全员").findOne());

		// 点击外勤打卡
		clickP(300, 1000);
	//}

	text("打卡").waitFor();
	cilckCenter(text("打卡").findOne());

	text("外勤打卡").waitFor();
	if (text("今日休息").exists()) {
		console.log("今日休息");
	} else {
		button = text("外勤打卡").findOne()
		if (button) {
    clickCenter(button)
			console.log("打卡成功");
		}
	}
}
main();

