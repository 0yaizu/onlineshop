document.addEventListener("DOMContentLoaded", function () {
	let lastClickedSubmit = null;
	document.querySelectorAll('form button[type="submit"], form input[type= "submit"]').forEach(function (btn) {
		btn.addEventListener("click", function () {
			lastClickedSubmit = this;
		});
	});
	document.querySelectorAll("form").forEach(function (form) {
		form.addEventListener("submit", function (e) {
			if (form.dataset.submitting === "1") {
				e.preventDefault();
				return;
			}
			form.dataset.submitting = "1";
			const preferSubmitByName = form.querySelector('[name="submit"][type = "submit"], button[name = "submit"][type = "submit"]');
			const firstSubmit = form.querySelector('button[type="submit"], input[type = "submit"]');
			const btn = (e.submitter) || lastClickedSubmit || preferSubmitByName ||
				firstSubmit;
			if (!btn) return;
			const isInput = btn.tagName === "INPUT" && btn.type === "submit";
			const getLabel = () => isInput ? btn.value : btn.textContent;
			const setLabel = (s) => {
				if (isInput) btn.value = s; else btn.textContent =
					s;
			};
			setLabel("Sending...");
			btn.disabled = true;
			setTimeout(() => {
				btn.disabled = false; setLabel(getLabel()); form.datas
				et.submitting = "0";
			}, 10000);
		});
	});
});