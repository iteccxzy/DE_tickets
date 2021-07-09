if ($(location).attr('href').includes("get_plans")) {

    import('./modules/plans.js')
        .then((module) => {
            let plan = module.loadplan();
        });

}
else if ($(location).attr('href').includes("get_stocks")) {

    import('./modules/stocks.js')
        .then((module) => {
            let stock = module.loadstock();
        });
}
else if ($(location).attr('href').includes("get_orders")) {

    import('./modules/orders.js')
        .then((module) => {
            let order = module.loadorder();

        });
}
else if ($(location).attr('href').includes("customer")) {

    async function loadmodule() {
        var module = await import('./modules/customers.js');
        let cust = module.loadcustomer();
    };

    loadmodule();

 

};