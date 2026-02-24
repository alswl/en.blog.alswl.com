---
title: "GitOps and Version Management"
slug: "gitops-and-version-management"
date: 2023-09-23T18:22:27+08:00
categories: ["coding"]
tags: ["Design", "Architecture"]
typora-copy-images-to: ../../static/images/202309
---

![car](../../static/images/202309/car.png)

<small>image via [shipvehicles](https://www.shipvehicles.com/step-by-step-guide-for-state-to-state-transport/)</small>

Using GitOps to manage delivery content is a common DevOps practice. We use Git for version control and Git tags to track the versions of deployed software. While this may seem to work, the concept of versioning is far from that simple in the age of cloud-native technology.

## The Version Problem

After introducing GitOps into the DevOps workflow, we can leverage GitOps for continuous integration and continuous delivery. GitOps addresses three core concerns: **content**, **version**, and **collaboration**. Yet we often focus on content and overlook version management.

What version-management issues need to be solved in a GitOps process?

A complete GitOps solution includes content description (Manifest), build strategy (Builder), and application strategy (Applier). Content description has given rise to many description languages, from traditional [Ansible](https://www.ansible.com/) / [Chef](https://www.chef.io/products/chef-infra) to cloud and cloud-native favourites like [Terraform](https://www.terraform.io/), [Helm](https://helm.sh/), and [Kustomize](https://kustomize.io/). With so many ways to describe content, pinning down an application’s version becomes very complex.

When we talk about version, do we <mark>mean the version of the application source code, the version of an image, or the version of an infrastructure-as-code (IaC) repository</mark>? Furthermore, when releasing a set of related applications—e.g. frontend and backend, or a system made of multiple backend apps—how do we clearly describe the <mark>version dependencies</mark> between them?

Inaccurate versioning leads to problems such as wrong release versions, tangled application dependencies, and inability to roll back.

Many teams handle this vaguely: ship the latest version, deploy backend before frontend. In a complex product team or one that must maintain multiple stable versions, this rough approach is not acceptable.

Version management addresses not only <mark>version identification</mark> but also <mark>dependencies</mark> between applications. GitOps version management therefore needs to answer:

- How to build artifacts delivered to customers, how to define their versions, and how to present all versions.
- How to resolve version dependencies when a set of software has them.
- How to describe a system when a set of software forms one.

Version management is important for any delivered product. We will break down this topic step by step and move from the original questions to GitOps version-management best practices.

## A Brief Introduction to GitOps

Before going further, here is a short overview of GitOps so we share the same understanding of key concepts.

The core idea of GitOps is <mark>infrastructure as code (IaC)</mark>: using declarative descriptions instead of imperative ones. IaC content is usually based on some paradigm that describes the desired state of a target. That paradigm can be Terraform, Kubernetes YAML, [Pulumi](https://www.pulumi.com/), or even Ansible. The target can be cloud services, Kubernetes, or physical machines. In short, by using YAML instead of Bash scripts, we can greatly improve the accuracy and controllability of changes.

For GitOps, whether you use Git is not the main point; you could use SVN. Git is simply more widely used and fits well with team collaboration and CI/CD. With a Git repository, you also get versioning based on Git revision / tag / branch, which in practice means version history and managing multiple versions in parallel.

Describing things only by Git revision is still not enough for real-world needs.

## The Root of the Problem — Versions of Binaries and Startup Config

When we trace versions to their source, the most primitive version is the version of the code.

What is the version of the code? Is it the version in the code repository or the version of the application built from that code? This version is not the version in the version-control system (e.g. Git / Mercurial / SVN). Although the two are often related, the code itself is just a set of files; once a build succeeds, there is a version. If it is not defined, the version is unknown and not tied to the repository.

> Note: From here on we do not distinguish between Git / Mercurial / SVN; we use Git as the stand-in for all of them.

Also note that in Chinese there are two concepts (库 Library and 仓库 Repository). In neither case does it imply that a “library” must be a versioned (Git/SVN) repository—we are not assuming code is always under version control. When we pack source files into a zip (e.g. GitHub’s zip download), that zip is still a codebase even if it has lost all Git history.

The version of the code is effectively the <mark>version of the application</mark>, as intended by the author. It is usually in the form `vx.y.z` rather than a Git commit hash, and the most common approach is [semantic versioning](https://semver.org/).

I recommend storing the version in a `VERSION` file in the code tree. For example, Git’s [Version](https://github.com/git/git/blob/master/GIT-VERSION-GEN) file clearly shows the current version:

```
GVF=GIT-VERSION-FILE
DEF_VER=v2.42.GIT
```

The `.GIT` suffix indicates the code is in development mode. If we switch to a release, e.g. [v2.39.3](https://github.com/git/git/blob/v2.39.3/GIT-VERSION-GEN), we see `DEF_VER=v2.39.3`, a standard artifact version. Two best practices here:

- Use a file to store the source version.
- The version file in source is always in `dev` mode; it becomes an official version only after a release tag.

The output of the source is not only binaries, executables, and dynamic libraries (`.dll` / `.so` / `.dylib`) but also the corresponding startup configuration files. These configs are usually managed together with the version—e.g. Nginx’s `nginx.conf` and Redis’s `redis.conf` should be under version control.

What is built from the source repository is the **artifact**. Artifacts already have two versions:

- Source version, i.e. the version defined in the `VERSION` file.
- Source repository version, i.e. Git revision.

## Artifact Version Management

With artifact version management, things get more complex because artifacts introduce more questions:

- What is an artifact and what does it consist of? (Answered above.)
- How is an artifact installed? What is the installer and what is the runtime?
- How is artifact information managed centrally? How is data managed?
- Do artifacts depend on each other? How are dependencies and version constraints handled?

The concept of artifact is central. One key idea: <mark>artifacts can be turned into new artifacts by packers</mark>.

Because artifacts have versions and new artifacts get new versions, we end up with multiple layers. To avoid losing the original version, we extend the notion of version to <mark>Upstream Version</mark>—the version assigned by the software author, the source of all versions.

Why can one artifact become another? Consider containers in Kubernetes. A container is a delivery format: it puts the executable and startup config into an image that can run in a container environment. The image in a registry is itself an artifact.

Helm / Kustomize are also delivery formats (packaging toolchains). Each layer solves a specific problem and can run in a given environment (e.g. container, Kubernetes, cloud infrastructure).

Every artifact is built and has its own <mark>packaging info</mark>, which can change and thus add another version. In practice we want the artifact’s version tied to its upstream version. Each packaging mechanism may have its own config but should still follow the upstream version. For example, a Kubernetes Workload references an image; the Workload description is extra info, while the image remains under upstream control.

<mark>Artifact + Packaging Info = New Artifact</mark>. Artifacts are packed into new artifacts until the final installer deploys them into the target environment.

When these artifacts can be described in files (IaC), we get various IaC repositories, which are the core objects of GitOps.

## Concepts at a Glance

Here is a concise map of these concepts:

| Chinese      | English            | Explanation                                                                                                            |
| ------------ | ------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| 源代码       | Source Code        | The set of source files for a program or application                                                                   |
| 代码仓库     | Source Code Repo   | The unit of version control that holds the source code                                                                 |
| 版本         | Version            | Application version corresponding to the source; human-defined, semantic; sometimes called Upstream Version            |
| 可执行文件   | Executable File    | Build output, usually an ELF executable or a library                                                                   |
| 启动配置文件 | Configuration File | Startup config for the ELF/Lib, distinct from general config (e.g. Kubernetes YAML)                                    |
| 制品         | Artifact           | A set of executable + startup config that can run in a runtime; usually file-based; artifacts can nest other artifacts |
| 安装器       | Installer          | Tool that installs the artifact into the runtime                                                                       |
| 运行时       | Runtime            | Environment where the artifact runs, e.g. an OS, Kubernetes, Docker Engine                                             |
| 打包器       | Packer             | Tool that packs artifacts into a given format (new artifact)                                                           |
| 打包附属信息 | Packaging Info     | Extra info needed when packing, e.g. container OS, process resources, default env vars                                 |

Together these concepts form the core of artifact version management and help us manage and trace versions and their relationships.

### Packer

A packer is a tool that turns artifacts into a specific format via packaging (compile, link, merge, archive, etc.), producing a new artifact. Its input is usually upstream—either source code or artifacts produced by another system.

For example, when packaging Docker Compose, the input is images; for Helm, the input includes images, startup config, and Helm templates, and the output is YAML.

### Artifacts

An artifact is a collection of data that can run in a given environment. It is made of executables and startup config, usually as files, and runs in a runtime. Artifacts can nest other artifacts.

The most common form is a binary (ELF); it can also be something that runs in a specific environment, such as a container image. Artifacts are typically transferred as files.

### Installer

An installer is a tool that puts an artifact into a runtime. It deploys the artifact and ensures it runs. Examples: dpkg, Pacman, or self-extracting installers on Windows. For Kubernetes, we use `kubectl`; Helm uses the `helm` command.

## Linux Community Practice

Once we understand these concepts, we may notice how close they are to what the Linux community has been doing for years. Setting aside cloud-native buzzwords, the Linux world already had a full solution.

Each layer of artifacts introduces new config / extension / values / env vars—we call all of this **configuration**. This packaging info brings its own challenges at scale.

> Proudly using Arch Linux.

### Arch Linux Practice

Arch Linux uses [Pacman](https://wiki.archlinux.org/title/Pacman) as the package installer and has a full [build system](https://wiki.archlinux.org/title/Arch_build_system). The [PKGBUILD](https://wiki.archlinux.org/title/PKGBUILD) describes how a package is built; it is a Bash subset and the core file for the package.

For versioning, Arch has a clear scheme and a full <mark>artifact nesting</mark> story. In `PKGBUILD`, `pkgver` is the upstream version (with normalisation such as `_` for `-` and timestamp format). `pkgrel` is the release number (not build number); it is incremented on each release to track Arch releases. When most of the `PKGBUILD` changes, the release number changes. `epoch` is a last-resort mechanism to force a newer version by breaking version comparison; it defaults to 0 and is hidden.

`PKGBUILD` also uses versioned dependencies to handle modules. For example, the `base-devel` package depends on 26 base packages, and [that package itself](https://gitlab.archlinux.org/archlinux/packaging/packages/base-devel/-/blob/main/PKGBUILD) has <mark>no content</mark>. This avoids introducing a separate model (e.g. Group / Product).

## GitOps-Based Version Management

Back to GitOps version management: with the analysis above, can we answer the original questions?

- How are customer-facing artifacts composed, how do we define their version, and how do we present all versions?
  - Use a `VERSION` file for the software (upstream) version.
  - Each artifact form has its own version, tied to upstream—e.g. `v1.2.3-afe12c` for the Git repo, `v1.2.3-afe12c-b1` for the image build.
- How do we resolve version dependencies within a set of software?
  - Leave this to the installer; the metadata is usually in the packaging info and consumed by the installer.
- How do we represent a system formed by a set of software?
  - Create a new artifact with no upstream version; its content may be empty but it carries packaging and dependency info.
  - Alternatively, introduce a dedicated concept; that depends on how the packer and installer work together.

## Summary

The wisdom of version management is already present in RPM / DEB / PKGBUILD. We give the application author the right to define version, we allow artifact nesting, and we let versioning span multiple layers.

We want the version of the running artifact to still be derived from the original application (Upstream) version. In large-scale cluster management, it matters that every running program knows where it came from and what it is.
