#include <stdio.h>

//gcc -fPIC -shared -rdynamic hi.c -o  hi1.so


int kk1()
{
    printf("kk1 = 1\n");
    return(1);
    }

int kk10(int addkk)
{
    int kk_res;
    kk_res = addkk+10;
    printf("kk10 = %d\n", kk_res);
    return(kk_res);
    }


int plugin_init(char *params_list)
{
    printf("plugin_init params_list = %s", params_list);
    return (10);
    }

int plugin_run_function(char *params_list)
{
    printf("plugin_run_function = %s", params_list);
    return (11);
    }



int main()
{
    int kk;
    kk=kk10(11);
    printf("kk = %d\n", kk);
    printf("Hi\n");
    return(0);
    }
    

