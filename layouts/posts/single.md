{{/* replace
adapter for local / server view images, local using ../../static, and remote use /
https://medium.com/@ardianta/writing-using-typora-on-hugo-based-blog-a1be8500774a
replace
![title](../../static/images/image.jpg)
to
![title](/images/image.jpg)
*/}}
{{ replaceRE `!\[([^\]]+)\]\(\.\./\.\.\/static\/(images\/[^\)]+)\)` "![$1](/$2)" .RawContent }}
