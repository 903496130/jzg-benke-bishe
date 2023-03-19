function showLoading() {
	div =
		'<div id="jzg-loadingMain"><div id="jzg-loading" onclick="rotate()"><div id="jzg-back"><span id="jzg-left"></span><span id="jzg-right"></span></div><span id="jzg-point"></span><span id="jzg-point2"></span><span id="jzg-front">Loading……</span></div></div>';
	$("body").append(div);
	// setTimeout(function(){
	// 	hideLoading();
	// },3000)
}

function hideLoading() {
	$("#jzg-loadingMain").css("transition", "1s");
	$("#jzg-loadingMain").css("opacity", "0");
	setTimeout(function() {
		$("#jzg-loadingMain").remove();
	}, 1000)
}

function toast(string) {
	$("#toast").remove();
	div = '<div id="toast"></div>';
	$("body").append(div);
	if (string != "") {
		$("#toast").html(string);
		$("#toast").css("opacity", "1");
		setTimeout(function() {
			$("#toast").css("opacity", "0");
		}, 2000)
		setTimeout(function() {
			$("#toast").remove();
		}, 2000)
	}

}
