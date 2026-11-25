# 碎面清理 FragClean · ZBrush 插件

> 嗨～我是「碎面清理」！我会帮你把 ZBrush 子工具里那些偷偷离家出走的小碎面一个个找回来、清干净，让你的打印件清清爽爽、安安心心地去做布尔～

在 3D 打印件做布尔运算前，自动检测并删除子工具里与主体分离的细碎小面片。
一键替代手动流程：独立显示 → 封闭孔洞 → 自动分组 → Ctrl+Shift 点选主体 → 删除隐藏。

- 支持 **ZBrush 2022.0.5** 和 **ZBrush 2025.0.1**（实测通过；2023 / 2024 按 2025 版安装，未实测）
- **中文版**（Z插件 → 碎面清理）和 **英文版**（ZPlugin → FragClean），功能完全一样
- 可以只处理当前子工具，也可以批量处理所有可见子工具
- 先「检测」看看有几块碎面，不改模型；确认后再「清理」

> 觉得好用的话，点个 ⭐ Star 支持一下 · If you find it useful, please give it a ⭐ Star!

## 安装

1. 下载并解压（GitHub 页面右上 **Code → Download ZIP**，或在 Releases 里下载）。
2. 双击 `install.bat`，选 **1 = 中文** 或 **2 = English**。
   找不到 ZBrush 时，把 ZBrush 的安装文件夹拖进窗口按回车即可。
3. 打开 ZBrush，按 **Ctrl+Shift+L**，选 `ZStartup\ZPlugs64\FragClean.txt` 加载一次。以后每次启动都会自动加载。
4. 在左侧 **Z插件 → 碎面清理** 里使用。

## 使用前请注意

- **清理前先保存 ZTL。**
- 清理后会丢失 **图层** 和 **形变目标**；**UV、多边形组**、子工具名称、位置和文件夹都会保留。
- 有细分级别的子工具不能处理，插件会弹窗提醒，请先删除细分级别。
- 每次启动 ZBrush 后第一次清理，ZBrush 会弹「这不是可撤销操作」，请点 **「始终确定」**。

完整说明：[使用说明.md](使用说明.md) · English guide: [USER_GUIDE_EN.md](USER_GUIDE_EN.md)

## 原理

复制子工具 → 拆分成组件（Split To Parts）→ 统计每块面数，最大的是主体，达到「保留比例%」的块也保留 → 删除其余碎块、合并保留块 → 导出 OBJ 再导入回原子工具。

## 修改 / 构建

插件源码由 `generate_plugin.py` 生成（ZScript 源文件必须是纯 ASCII，中文在运行时用 `StrFromAsc` 拼出）：

```
python generate_plugin.py
```

生成 `build/{zh,en}/{2025,2022}/FragClean.txt`。`test/` 里有测试用的 OBJ 模型。

---

## English

**FragClean** finds and deletes small loose pieces that are not connected to the main body of a ZBrush SubTool — a quick check before Boolean operations on 3D-print parts. It works on the selected SubTool or on every visible SubTool, and comes in English and Chinese versions.

Install: run `install.bat`, choose **2 = English**, then in ZBrush press **Ctrl+Shift+L** and load `ZStartup\ZPlugs64\FragClean.txt` once. The buttons are in **ZPlugin > FragClean**. See [USER_GUIDE_EN.md](USER_GUIDE_EN.md).

Tested on ZBrush 2022.0.5 and 2025.0.1.

## License

[MIT](LICENSE)
