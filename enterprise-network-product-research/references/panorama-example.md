# Aruba全景图示例

`panorama_masked.svg`、`panorama_masked.png` 现在是独立生成的Aruba CX八型号布局示例，文件名保留以兼容SKILL引用。只用于展示信息结构（横向分层、接口/容量摘要及同能力SKU差异），不得作为风格/配色模板；实际字体、色彩和外观由Agent运用前端设计能力独立决定。示例含历史Bundle记录以演示差异，不代表当前纳入政策：实际研究按SKILL排除Bundle及其子SKU，不能照搬示例型号清单。它不是厂商完整目录或权威参数库，不代表HPE官方制作或背书。

生成输入见 `panorama-example.json`：每款保留示例文字和官网定位URL；来自已有Aruba研究输入，未在此次制图中重新核验所有链接和参数。TAA未标明不等于不符合，电源制式缺失不默认AC，接口/容量不能直接用于选型排名。例图不含旧私有参考的型号、数据、产品数量、代际规划或降本关系，也未读取旧图作为生成输入。

从技能根目录重建：

```sh
python3 -I -B scripts/render_panorama_example.py --font /path/to/licensed-chinese-sans-font.ttf
```

Python 3仅依赖标准库；生成PNG另需ImageMagick。字体由运行环境提供，不随仓库分发。SVG保留可选文字和回退字体，不含嵌入字体、外部图片、脚本或外部样式。不要将实际原始产品资料/内部参考图放回此文件名。

PNG与SVG须同源生成；发布检查需核实示例标记、来源边界、字体显示和无旧参考残留。此说明只覆盖这两张新参考及其数据/生成器，不构成整个仓库已完成公开审查的保证。
