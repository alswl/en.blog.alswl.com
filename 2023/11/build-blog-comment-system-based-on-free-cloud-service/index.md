

## The Problem

After migrating the blog from WordPress to a static site in 2012, I chose Disqus as the comment system.
Recently, Disqus ads have become too intrusive, so I urgently need to <mark>find a new comment system</mark>.

[Disqus officially](https://help.disqus.com/en/articles/1717119-ads-faq) states that removing ads requires a paid subscription.

> What if I want to remove Ads?
> If you'd like to remove Disqus Ads from your integration, you may purchase and ads-free subscription from your Subscription and Billing page. More information on Disqus ads-free subscriptions may be found here.

OK, goodbye Disqus—I'll find a reliable, free, and easy-to-use comment system.
Since I'm looking for a new comment system anyway, and it's 2023 now,
I want this new system to <mark>fully leverage the convenience of cloud services</mark>, and to be
<mark>free, reliable, and easy to maintain</mark>.

![no-disqus-twitter](https://en.blog.alswl.com/img/202311/no-disqus-twitter.png)

## Selection Principles

Before diving in, I outlined my principles and selection criteria:

- **Data ownership is the core requirement**
  - Ensure comment data fully belongs to the blog owner, with no loss of control due to third-party services.
- **Deployment and storage are the main challenges**
  - Considering stability and cost, choose a solution that is easy to deploy and has low storage cost.
- **Access speed is a consideration**
  - Comment system load speed directly affects user experience,
    so a system that offers fast access is needed.

Functional requirements:

- Email notifications
- Markdown
- Content safety: No Injection
- Comment moderation and deletion
- OAuth login (optional)

Non-functional requirements:

- Low cost: within 12 CNY/year
- System stability

With these principles and requirements clear, we can choose a suitable comment system in a more targeted way. Next, I'll explore how to select and set up a comment system based on these principles.

## Initial Exploration

Now let's try out some options and explore, to get familiar with the <mark>features and quality</mark> of common systems today.

### [utterances](https://utteranc.es/)

![utterances](https://en.blog.alswl.com/img/202311/utterances.png)

- A comment system often seen in the wild, popular among developers; based on GitHub Issues, so it's free; requires GitHub account to comment.
- 7.8k stars
- Hosted on GitHub Issues

### [Twikoo](https://twikoo.js.org/quick-start.html)

![twikoo](https://en.blog.alswl.com/img/202311/twikoo.png)

- A solution from China, built around cloud services; requires a serverless/cloud function environment (most are paid).
- 880 stars

### [Cusdis](https://cusdis.com/)

![cusdis](https://en.blog.alswl.com/img/202311/cusdis.png)

- A solution from China; offers free Cloud service (with limited quota).
- 2.4k stars
- Supports migration
- Manual comment approval
- Moderate activity

I also looked at some external comparison articles:

- [Comments | Hugo](https://gohugo.io/content-management/comments/)
- [静态博客评论系统的选择 - 腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/2196035?areaSource=&traceId=)
- [轻量级开源免费博客评论系统解决方案 （Cusdis + Railway） - 少数派](https://sspai.com/post/73412)

From this exploration, the deployment model looks roughly like this:

![comment-system-deploy-diagram](https://en.blog.alswl.com/img/202311/comment-system-deploy-diagram.png)

## Comparison

Here is a comparison table of features I care about and how each candidate performs. Besides the systems above,
I also looked into <mark>comment SaaS services commonly used overseas</mark>:

| Name            | self-host | Official SaaS | SaaS Free   | Star | Import Disqus | export data | Comments                                   |
| --------------- | --------- | ------------- | ----------- | ---- | ------------- | ----------- | ------------------------------------------ |
| Utterances      | x         | v             | v           | 7.8k |               | v           | Github account required                    |
| Cusdis          | v         | v             | v?          | 2.3k | v             | v?          | import from Disqus failed                  |
| Cactus Comments | v         | v             |             | 100  |               |             | Matrix Protocol, blocked                   |
| Commento        | x         | v             | $10/month   |      | v             | v           |                                            |
| Graph Comment   |           | v             | Free to $7  |      |               |             |                                            |
| Hyvor Talk      | x         | v             | $12/month   |      |               |             |                                            |
| IntenseDebate   |           | v             | ?           |      | x             |             | too old                                    |
| Isso            | v         | x             |             | 4.8k | v             |             | sqlite storage                             |
| Mutt            |           | v             | $16/month   |      |               |             |                                            |
| Remark42        | v         | x             |             | 4.3k | v             | v           | full featured, one file storage            |
| ReplyBox        |           | v             | $5/month    |      |               |             |                                            |
| Staticman       | v         |               |             | 2.3k |               | v           | using github as storage                    |
| Talkyard        |           | v             | €4.5/ month |      |               |             |                                            |
| Waline          | v         |               |             | 1.5k | v             | v           | Multi Storage / Service Provider supported |
| Twikoo          | v         | x             |             | 1.1k | v             | v           | FaaS / MongoDB                             |

From this comparison we can draw a few conclusions:

- Traditional overseas comment systems have low data transparency and old-fashioned UIs.
- Official SaaS offerings are mostly paid.
- Self-hosted options require running your own service, with no one-click free cloud path.

**Summary**

The products that best fit my needs are: Utterances, Cusdis, and Waline.

## PoC and Implementation

I eventually chose Utterances and Waline for a PoC.
My [English blog](https://en.blog.alswl.com/) uses Utterances,
and my [Chinese blog](https://blog.alswl.com/) uses Waline.

Why not Cusdis or Twikoo? Cusdis uses PostgreSQL,
while Twikoo relies on Tencent Cloud Functions (limited free tier) or MongoDB.
Waline offers more storage options.
Among similar solutions, Waline has the most contributors and commits,
so the community is more reliable.

### Waline Implementation

> One funny detail: if the h3 heading here were "Waline", it would inject the comment widget for this blog right there.

- Pros
  - Multi-platform deployment
  - Multiple database backends (MongoDB, sqlite, PostgreSQL, MySQL)
  - Rich comment features
  - Import tools
  - Active enough
- Cons
  - Feature-heavy, not very minimal (but configurable)
  - Product from China
- Integration steps:
  - Choose a storage provider (I chose <mark>LeanCloud</mark>)
  - Choose a server provider for deployment (I chose <mark>Vercel</mark>)
  - Choose an email provider (I chose <mark>Brevo</mark> (formerly SendinBlue))
  - Frontend integration (embed in Hugo)

Deployment diagram:

![waline](https://en.blog.alswl.com/img/202311/waline.png)

For the actual steps, follow the official docs:

- [Quick Start | Waline](https://waline.js.org/guide/get-started/)
- [Deploy on Vercel | Waline](https://waline.js.org/guide/deploy/vercel.html#%E5%A6%82%0E4%BD%95%E9%83%A8%E7%BD%B2)
- Bind CNAME
- Import data
  - Convert with [Migration Tool | Waline](https://waline.js.org/migration/tool.html)
  - Import at https://console.leancloud.app/apps/yours/storage/import-export
- Page configuration
  - Disable some features via [client props](https://waline.js.org/reference/client/props.html)
  - Enable SMTP
    - Set `AUTHOR_EMAIL`
    - Set `SENDER_NAME`
    - Set `SENDER_EMAIL`
  - Server config: https://waline.js.org/reference/server/config.html#tgtemplate
- Issues I ran into
  - Disqus export does not include user emails, so Gravatar avatars don't show; no workaround
  - Email config needs extra env vars, otherwise your personal email can be exposed

Implementation PR (frontend only; backend contains secrets and isn’t shared):
[feat: comments on waline · alswl/blog.alswl.com@e34e348](https://github.com/alswl/blog.alswl.com/commit/e34e34810298fd0d716d4c4a467fada25b3a6622)

### Utterances Implementation

Utterances is even simpler to set up—a single PR enables it.
[feat: comment using utteranc · alswl/en.blog.alswl.com@29028f6 (github.com)](https://github.com/alswl/en.blog.alswl.com/commit/29028f677e362570a8bcaf5316847ddfa3e9d685)

Nothing fancy, just simplicity. Given the low traffic on my English blog, the minimal approach works.

## Summary

I ended up with Waline and Utterances as my comment systems; both have zero deployment cost.

I traded some access speed and security for better data control and a self-hosted setup.
In terms of stability, although the chain is more complex and a single node can fail,
relying on Vercel, LeanCloud, and Brevo keeps overall risk manageable.

After all, it’s just a small comment system—zero cost and “it works” is enough.

Feel free to try leaving a comment below.

