# Zenodo DOI 与 GitHub Release:操作清单

目标:给仓库一个**持久标识符(DOI)**,这样论文里可以写"数据与代码见 doi:10.5281/zenodo.XXXXXXX",审稿人和读者都能长期访问。

耗时约 15 分钟,不需要写代码。

---

## 第一步:确认许可证(已完成)

仓库根目录已有 `LICENSE`(MIT),覆盖 `analysis/`、`scripts/`、`docs/`、`data/`。
`LICENSE_DECISION_REQUIRED.md` 可以保留作为历史记录,或在 README 里注明已解决。

---

## 第二步:注册 Zenodo(如果还没有)

1. 打开 https://zenodo.org
2. 点右上角 **Sign up**,选择 **Sign up with GitHub**(用同一个 GitHub 账号,后面绑定最方便)
3. 授权后完成邮箱验证

> Zenodo 是 CERN 运营的,免费,GitHub 官方推荐。

---

## 第三步:把 GitHub 仓库连接到 Zenodo

1. 登录 Zenodo 后,点右上角头像 → **Settings** → 左侧 **GitHub**
2. 找到 **miyuheng297-hue/qace-materials-public**,把开关拨到 **ON**
3. 页面会提示:此后每次在 GitHub 创建 **Release**,Zenodo 会自动存档并生成 DOI

⚠️ 只有**开启之后**创建的 Release 才会被存档。之前的 tag (`public-materials-2026-08-17`) 不会追溯。

---

## 第四步:在 GitHub 创建一个 Release

1. 打开 https://github.com/miyuheng297-hue/qace-materials-public/releases/new
2. **Choose a tag** 下拉里已经有 `plos-one-2026-10`(已推送),直接选它;若下拉没有,手动输入同名字符串
3. **Release title** 填:`PLOS ONE submission package (2026-10-23)`
4. **Describe this release** 粘贴下面的内容:

```
Reproducibility package for the PLOS ONE submission.

Added:
- analysis/: count-matched comparison, rank reversal, TOST equivalence, threshold
  sensitivity, mechanism attribution, answer scoring, snapshot builder
- data/: candidate scores for the closed-pool and expansion-on conditions
  (hashed fact identifiers, no benchmark text), six per-selector selection
  records, per-question F1, full-coverage answer generations, 2Wiki aggregate
- docs/: REPRODUCTION.md, DATA_DICTIONARY.md
- LICENSE (MIT)

Scope: no benchmark sentence text, titles, questions or gold answers are
redistributed. Candidate facts are identified by sha256("title##index")[:16].
```

5. 点 **Publish release**

---

## 第五步:拿到 DOI

1. 回到 Zenodo → 左侧 **Upload** (或直接刷新 GitHub 页面后收到的邮件)
2. 几秒到几分钟后会出现一条新记录,标题是 `miyuheng297-hue/qace-materials-public`
3. 记录页会显示 **DOI: 10.5281/zenodo.XXXXXXX**

---

## 第六步:回填到论文(告诉我,我来改)

拿到 DOI 后,论文的 Data availability 段要改成:

> ...are publicly available at https://github.com/miyuheng297-hue/qace-materials-public
> and archived at doi:10.5281/zenodo.XXXXXXX.

同时 Zenodo 记录页可以补充:
- **Authors**:Jianhua Ren, Yuheng Mi
- **License**:MIT
- **Related identifiers**:填论文的 DOI(录用后)或期刊名

---

## 常见问题

**Q:Release 之后又改了代码怎么办?**
A:每次发新 Release 会得到新 DOI(版本 DOI),同时有一个**总 DOI** 指向最新版。论文里引用总 DOI。

**Q:仓库里有 HotpotQA 内容吗?**
A:没有。所有数据用 `fact_id = sha256("title##index")[:16]`,本地用公开数据集即可还原。评审若问起,这一点正是加分项。

**Q:Zenodo 要钱吗?**
A:免费,单个文件上限 50 GB。

**Q:能不能不发 Release,只靠 GitHub 链接?**
A:可以,但 PLOS 明确**鼓励**用带持久标识符的仓库;而且 GitHub 链接可能失效,DOI 不会。建议做。
