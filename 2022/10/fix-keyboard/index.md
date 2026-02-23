

![fu-tu-kang](https://en.blog.alswl.com/img/202210/fu-tu-kang.png)


> In order to be well prepared, how can I successfully join an electronics factory after graduating at the age of 35?
>
> Learn from fixing keyboards(it's a joke)



## Background



The keyboard I using is the ErgoDox, an ergonomically split keyboard. More details about ErgoDox can be found in my previous [answer](https://www.zhihu.com/question/52088337/answer/141073759).

![keyboard-view](https://en.blog.alswl.com/img/202210/keyboard-view.png)


(former keycap color scheme + hand rest).

![keyboard-view-2](https://en.blog.alswl.com/img/202210/keyboard-view-2.png)


After seven or eight years of work, it has been into the water, into the coffee, but also into the soy milk, now finally a few keys are not flexible, pressed a sticky feeling, can not provide a smooth coding feel.


After a few months of using a back up Filco, I finally made up my mind to get the ErgoDox fixed.

## Prepare

![prepare](https://en.blog.alswl.com/img/202210/prepare.png)


- Soldering Iron
- Solder Sucker
- Solder
- Key Shaft
- Seiko Screw Driver Kit
- Key Puller
- Cherry Key Switch Puller


For those without soldering experience, you can learn how to soldering.


[女生都能学会的键盘焊接换轴教程\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1xt4y157LM/)


[电烙铁的错误和正确使用方法\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1Ui4y177kk/)


## Processing

<center><mark><b>Check which key shafts to replace, press one and listen to one</b></mark></center>

![step-1](https://en.blog.alswl.com/img/202210/step-1.png)


<center><mark><b>Remove the shell</b></mark></center>

![step-2](https://en.blog.alswl.com/img/202210/step-2.png)


<center><mark><b>Remove the corresponding keycaps (note that F J keycaps are different)</b></mark></center>

![step-3](https://en.blog.alswl.com/img/202210/step-3.png)



<center><mark><b>Melt the solder and suck the melted solder away with a solder sucker</b></mark></center>


![step-4](https://en.blog.alswl.com/img/202210/step-4.png)



<center><mark><b>With a key switch puller, remove it from the front, remember there is a soft clip, to up and down direction (i.e. cherry logo direction + opposite force)</b></mark></center>

![step-5](https://en.blog.alswl.com/img/202210/step-5.png)


<center><mark><b>Look at the coffee and soy milk that went in</b></mark></center>

![step-6](https://en.blog.alswl.com/img/202210/step-6.png)



<center><mark><b>Weld the new key shaft on</b></mark></center>

![step-7](https://en.blog.alswl.com/img/202210/step-7.png)



<center><mark><b>Sucking away the debris spit out the look of the solder sucker</b></mark></center>

![step-8](https://en.blog.alswl.com/img/202210/step-8.png)



<center><mark><b>Final assembly</b></mark></center>

![keyboard-final](https://en.blog.alswl.com/img/202210/keyboard-final.png)



## Summary

I have that feeling of typing smoothly again ~

Youthfulness is back~




Finally, I'd like to share my ErgoDox Layout configuration:


-   [alswl/ergodox-firmware/blob/master/src/keyboard/ergodox/layout/alswl-layout.c](https://link.zhihu.com/?target=https%3A//github.com/alswl/ergodox-firmware/blob/master/src/keyboard/ergodox/layout/alswl-layout.c) My layout configuration, Five layouts：Normal / Funtion Key / Number Pad / MediaKey / Arrow
-   [alswl/ergodox-firmware/blob/master/src/main.c#L127](https://link.zhihu.com/?target=https%3A//github.com/alswl/ergodox-firmware/blob/master/src/main.c%23L127) configuration for LED, lighting on to indicated the different layout
-   [alswl/teensy_loader_cli](https://link.zhihu.com/?target=https%3A//github.com/alswl/teensy_loader_cli)[alswl/teensy_loader_cli](https://link.zhihu.com/?target=https%3A//github.com/alswl/teensy_loader_cli) teensy loader cli works for macSO, the ofiicial binary not works when press the reset button


If you get something out of it, give it a like.

