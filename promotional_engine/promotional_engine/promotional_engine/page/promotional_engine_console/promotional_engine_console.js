frappe.pages["promotional-engine-console"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Promotional Engine Console"),
		single_column: true,
	});

	const $body = $(`
		<div class="promotional-engine-console">
			<div class="row">
				<div class="col-md-12">
					<div class="alert alert-info">
						Satu halaman ini dirancang sebagai control tower untuk semua promo, kupon, poin, dan benefit POS.
					</div>
				</div>
			</div>
			<div class="row">
				<div class="col-md-3">
					<div class="standard-sidebar-item">
						<a href="/app/promotion-campaign">Campaigns</a>
					</div>
				</div>
				<div class="col-md-3">
					<div class="standard-sidebar-item">
						<a href="/app/promotion-rule">Rules</a>
					</div>
				</div>
				<div class="col-md-3">
					<div class="standard-sidebar-item">
						<a href="/app/coupon-batch">Coupon Batches</a>
					</div>
				</div>
				<div class="col-md-3">
					<div class="standard-sidebar-item">
						<a href="/app/loyalty-policy">Loyalty Policies</a>
					</div>
				</div>
			</div>
		</div>
	`);

	$(page.body).append($body);
};
