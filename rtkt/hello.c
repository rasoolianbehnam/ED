#include <linux/param.h>
#include <linux/module.h>
#include <linux/kernel.h>
//#include <linux/system.h>

static int load(struct module *module, int cmd, void *arg) {
    int error = 0;

    switch (cmd) {
        case MOD_LOAD:
            uprintf("Hello, world!\n");
            break;
        case MOD_UNLOAD:
            uprintf("Goodbye, cruel world!\n");
            break;
        default:
            error = EOPNOTSUPP;
            break;
    }
    return error;
}

static moduledata_t hello_mod = {
    "hello",
    load,
    NULL
};

DECLARE_MODULE(hello, hello_mod, SI_SUB_DRIVERS, SI_ORDER_MIDDLE);
