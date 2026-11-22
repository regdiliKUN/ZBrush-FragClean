# -*- coding: utf-8 -*-
"""
生成 ZBrush 插件 FragClean（碎面检测/清理）的 ZScript 源文件，中英两个语言版本。

ZScript 编译器会丢掉非 ASCII 字面量，所以 .txt 必须是纯 ASCII，
中文提示在运行时用 [StrFromAsc, UTF-8字节] 拼出来。改文字就改下面的 TEXT 字典
（每项 = (English, 中文)），然后运行:  python generate_plugin.py
输出: build/zh/{2025,2022}/FragClean.txt  和  build/en/{2025,2022}/FragClean.txt
两个语言文件同名，安装哪个就用哪个（install.bat 会让你选）。
注意 ZScript 字符串上限 255 字节，中文每字 3 字节，一条提示别超过约 70 个汉字。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- UI text (English, 中文)
TEXT = {
    # 插件面板名 / 按钮 / 控件标签（加载时设置）
    "L_PAL":    ("FragClean",       "碎面清理"),
    "L_DET1":   ("Detect Current",  "检测当前"),
    "L_DETA":   ("Detect All",      "检测全部可见"),
    "L_CLN1":   ("Clean Current",   "清理当前"),
    "L_CLNA":   ("Clean All",       "清理全部可见"),
    "L_HOLE":   ("Close Holes",     "先封闭孔洞"),
    "L_KEEP":   ("Keep %",          "保留比例%"),
    # 提示（tooltip）
    "T_DET1":   ("Count the loose pieces of the selected SubTool. The model is not changed.",
                 "只检测当前子工具有几块与主体分离的碎块，不修改模型。"),
    "T_DETA":   ("Check every visible SubTool and show a summary. The models are not changed.",
                 "逐个检测所有可见子工具，不修改模型，最后汇总报告。"),
    "T_CLN1":   ("Keep the largest connected piece (and pieces above Keep %) and delete the rest. Name and position are kept.",
                 "清理当前子工具：保留最大的连通块（及达到保留比例的块），删除其余碎块。名称、位置、文件夹不变。"),
    "T_CLNA":   ("Clean every visible SubTool. Save your ZTL first.",
                 "对所有可见子工具执行清理。建议先保存 ZTL。"),
    "T_HOLE":   ("Run Close Holes before cleaning, as in the manual workflow.",
                 "清理前先执行 封闭孔洞（Close Holes），与手动流程一致。"),
    "T_KEEP":   ("Pieces with at least this percent of the largest piece's faces are kept too. 100 = keep only the largest.",
                 "面数达到最大块该百分比的块也保留（如双眼这类有意分开的部件）。100 = 只保留最大块。"),
    # 运行时消息
    "M_EDIT":   ("Turn on Edit mode (press T) first.",
                 "请先进入 Edit 编辑模式（按 T 键），再运行。"),
    "M_MISS":   ("These ZBrush buttons were not found, the plugin cannot run:",
                 "找不到以下 ZBrush 按钮，插件无法运行："),
    "M_SDIV":   ("has subdivision levels - skipped",
                 "有细分级别，已跳过"),
    "M_SDV1":   ("This SubTool has subdivision levels:",
                 "当前子工具有细分级别："),
    "M_SDV2":   ("These SubTools have subdivision levels:",
                 "以下子工具有细分级别："),
    "M_SDV3":   ("Remove them first: Geometry > Del Lower / Del Higher.",
                 "请先取消细分级别（几何体 → 删除低级 / 删除高级）。"),
    "M_SDV4":   ("They will be skipped. Continue with the others?",
                 "它们会被跳过。继续处理其余子工具吗？"),
    "M_FAIL":   ("split failed - skipped",
                 "拆分失败，已跳过"),
    "M_IMPF":   ("write-back failed: result left in the SubTool below it",
                 "回写失败：清理结果留在其下方的子工具里，请手动检查"),
    "M_CLEAN":  ("clean",
                 "无碎块"),
    "M_FRAG":   (" loose pieces",
                 "个分离碎块"),
    "M_DEL":    ("deleted ",
                 "已删除碎块 "),
    "M_KEPT":   (" pieces / kept ",
                 "，保留块 "),
    "M_FACES":  (" / faces ",
                 "，面数 "),
    "M_SUM1":   ("Check finished. SubTools checked: ",
                 "检测完成。共检查 "),
    "M_SUM2":   (" / with loose pieces: ",
                 " 个子工具，其中 "),
    "M_SUM3":   (".",
                 " 个有碎块。"),
    "M_SUMC1":  ("Clean finished. SubTools processed: ",
                 "清理完成。共处理 "),
    "M_SUMC2":  (" / pieces deleted: ",
                 " 个子工具，共删除碎块 "),
    "M_SUMC3":  (". Ctrl+Z to undo.",
                 " 块。可用 Ctrl+Z 撤销。"),
    "M_MORE":   ("Press OK to see the details per SubTool.",
                 "点「知道了」查看每个子工具的明细。"),
    "M_ASK":    ("Delete the loose pieces of every visible SubTool? Save your ZTL first.",
                 "将清理所有可见子工具中的分离碎块。建议先保存 ZTL。继续吗？"),
    "M_OK":     ("OK",
                 "知道了"),
    "M_YES":    ("Continue",
                 "继续"),
    "M_NO":     ("Cancel",
                 "取消"),
    "M_ABORT":  ("a confirmation was cancelled - stopped. Run again and choose Always OK.",
                 "确认框被取消，已停止（请重新运行并点「始终确定」）"),
    "M_FIRST1": ("First run: ZBrush will ask 'This is not an undoable operation'.",
                 "首次运行会弹「这不是可撤销操作」确认框："),
    "M_FIRST2": ("Choose 'Always OK' each time (valid until ZBrush restarts).",
                 "请都点「始终确定」（重启 ZBrush 前不再弹）。"),
    "M_FIRST3": ("If 'Mesh does not contain multiple parts' appears, click it to close.",
                 "若弹「网格不含多个部分」，点它关闭即可。"),
    "M_PROG":   ("Checking pieces ",
                 "碎面检查中 "),
    "M_ONE":    ("Selected SubTool:",
                 "当前子工具："),
}


def strmerge_chain(var, text):
    """把中文 text 变成若干行 [VarSet,var,[StrMerge,...]]，每个 StrMerge 不超过 10 个参数。"""
    bs = list(text.encode("utf-8"))
    lines = []
    first = True
    i = 0
    while i < len(bs) or first:
        if first:
            chunk = bs[i:i + 10]
            i += 10
            parts = ",".join("[StrFromAsc,%d]" % b for b in chunk)
            lines.append("[VarSet,%s,[StrMerge,%s]]" % (var, parts if parts else '""'))
            first = False
        else:
            chunk = bs[i:i + 9]
            i += 9
            parts = ",".join("[StrFromAsc,%d]" % b for b in chunk)
            lines.append("[VarSet,%s,[StrMerge,#%s,%s]]" % (var, var, parts))
    return lines


def text_lines(var, lang):
    """Lines that set var to its text in the given language."""
    en, zh = TEXT[var]
    if lang == "en":
        assert '"' not in en and len(en.encode()) < 250, var
        en.encode("ascii")
        return ['[VarSet,%s,"%s"]' % (var, en)]
    return strmerge_chain(var, zh)


def build(iconfig, lang):
    out = []
    w = out.append
    w("// FragClean - ZBrush SubTool loose-fragment detector / cleaner.")
    w("// GENERATED by generate_plugin.py - edit the generator, not this file.")
    w("// Pure ASCII source; Chinese strings are built with StrFromAsc at runtime.")
    w("// Targets ZBrush 2022.0.5 and 2025.0.1.")
    w("//")
    w("// Method per SubTool S (index FCIDX):")
    w("//   (clean) optional Close Holes on S")
    w("//   Duplicate S -> D (directly below), Split To Parts on D -> parts")
    w("//   detect: count parts, delete them all")
    w("//   clean : keep the largest part (+ parts >= Keep% of it), delete the rest,")
    w("//           merge the kept ones, export it solo to OBJ, import into S")
    w("//           (S keeps name / position / folder), delete the helper.")
    w("")
    w("[IConfig,%s]" % iconfig)
    w("")
    # numeric / string globals
    nums = ["FCIDX", "FCMODE", "FCN", "FCI", "FCJ", "FCK", "FCST", "FCF", "FCRET", "FCBASE",
            "FCPARTS", "FCBEST", "FCBESTF", "FCTHR", "FCKEPT", "FCRES", "FCDEL", "FCTOT",
            "FCHIT", "FCSUMDEL", "FCORIG", "FCVC", "FCKEEPIDX", "FCMISS", "FCLEN", "FCANS",
            "FCLISTN", "FCVISN", "FCQ", "FCCNT", "FCABORT", "FCWARNED", "FCSUMF", "FCKEEPEND", "FCOI", "FCSPLITOK", "FCP", "FCSDN"]
    for n in nums:
        w("[VarDef,%s,0]" % n)
    w("[VarDef,FCSTAT(256)]")
    w("[VarDef,FCVIS(256)]")
    w("[VarDef,FCKEEPF(4001)]")
    w('[VarDef,FCLINES(100),""]')
    strs = ["FCPAGE", "FCDIR", "FCTMP", "FCNL", "FCPAL", "FCHOLEPATH", "FCKEEPPATH", "FCB1", "FCB2", "FCB3", "FCB4", "FCMSG", "FCREP", "FCNAME", "FCLINE", "FCOBJ", "FCPATH", "FCMISSTXT"]
    for s in strs:
        w('[VarDef,%s,""]' % s)
    w('[VarSet,FCDIR,"C:/Users/Public/Documents/ZBFragClean/"]')
    w("")
    w("// ---- UI strings (%s) ----" % lang)
    for k in TEXT:
        w('[VarDef,%s,""]' % k)
    w("")
    w("// Labels are needed at load time (top level).")
    for k in TEXT:
        if k.startswith("L_") or k.startswith("T_"):
            out.extend(text_lines(k, lang))
    w("")
    w("[RoutineDef,FCInitStrings,")
    for k in TEXT:
        if k.startswith("M_"):
            for line in text_lines(k, lang):
                w("  " + line)
    w("]")
    w("")
    w(BODY)
    return "\n".join(out) + "\n"


BODY = r'''
// -------------------------------------------------------------- helpers
[RoutineDef,FCNote,
  [NoteIButton,#M_OK,,,,,,,,,0xffffff,,,]
  [VarSet,FCANS,[Note,#FCMSG,,,0x1f1f1f,,560,,,,,,]]
]

// Face count of the selected SubTool -> FCF
[RoutineDef,FCFaces,
  [VarSet,FCF,0]
  [VarSet,FCRET,[Mesh3DGet,1,,,FCF]]
  [If,(FCF<=0),[VarSet,FCF,FCRET]]
]

// Name of the selected SubTool (without the trailing dot) -> FCNAME
[RoutineDef,FCGetName,
  [VarSet,FCNAME,[IGetTitle,"Tool:ItemInfo"]]
  [VarSet,FCLEN,[StrLength,#FCNAME]]
  [If,(FCLEN>1),
    [VarSet,FCTMP,[StrExtract,#FCNAME,(FCLEN-1),(FCLEN-1)]]
    [If,([StrFind,".",#FCTMP]=0),[VarSet,FCNAME,[StrExtract,#FCNAME,0,(FCLEN-2)]]]
  ]
]

// Subdivision check of every visible SubTool (FCVIS snapshot) before a batch.
// Shows one reminder; FCRES = 0 when the user cancels or nothing is left.
[RoutineDef,FCSdivScanAll,
  [VarSet,FCSDN,0]
  [VarSet,FCPAGE,""]
  [VarSet,FCI,0]
  [Loop,FCN,
    [If,(FCVIS(FCI)=1),
      [SubToolSelect,FCI]
      [If,([IGetMax,"Tool:Geometry:SDiv"]>1),
        [VarInc,FCSDN]
        [RoutineCall,FCGetName]
        [If,([StrLength,#FCPAGE]+[StrLength,#FCNAME])<70,
          [If,([StrLength,#FCPAGE]>0),[VarSet,FCPAGE,[StrMerge,#FCPAGE,", "]]]
          [VarSet,FCPAGE,[StrMerge,#FCPAGE,#FCNAME]]
        ,
          [If,([StrFind,"...",#FCPAGE]<0),[VarSet,FCPAGE,[StrMerge,#FCPAGE," ..."]]]
        ]
      ]
    ]
    [VarInc,FCI]
  ]
  [If,(FCORIG<[SubToolGetCount]),[SubToolSelect,FCORIG]]
  [If,(FCSDN>0),
    [If,(FCSDN>=FCVISN),
      [VarSet,FCMSG,[StrMerge,#M_SDV2,#FCNL,#FCPAGE,#FCNL,#M_SDV3]]
      [RoutineCall,FCNote]
      [VarSet,FCRES,0]
    ,
      [NoteIButton,#M_YES,,,,,,,,,0xffffff,,,]
      [NoteIButton,#M_NO,,,,,,,,,0xffffff,,,]
      [VarSet,FCANS,[Note,[StrMerge,#M_SDV2,#FCNL,#FCPAGE,#FCNL,#M_SDV3,#FCNL,#M_SDV4],,,0x1f1f1f,,600,,,,,,]]
      [If,(FCANS!=1),[VarSet,FCRES,0]]
    ]
  ]
]

// Delete the SubTool at index FCK (confirm dialog auto-accepted)
[RoutineDef,FCDeleteAt,
  [VarSet,FCCNT,[SubToolGetCount]]
  [SubToolSelect,FCK]
  [IPress,"Tool:SubTool:Delete"]
  [If,([SubToolGetCount]=FCCNT),[VarSet,FCABORT,1]]
]

[RoutineDef,FCCheckButtons,
  [VarSet,FCMISS,0]
  [VarSet,FCMISSTXT,""]
  [If,[IExists,"Tool:SubTool:Duplicate"],,[VarInc,FCMISS][VarSet,FCMISSTXT,[StrMerge,#FCMISSTXT," Duplicate"]]]
  [If,[IExists,"Tool:SubTool:Split To Parts"],,[VarInc,FCMISS][VarSet,FCMISSTXT,[StrMerge,#FCMISSTXT," Split To Parts"]]]
  [If,[IExists,"Tool:SubTool:Delete"],,[VarInc,FCMISS][VarSet,FCMISSTXT,[StrMerge,#FCMISSTXT," Delete"]]]
  [If,[IExists,"Tool:Geometry:Close Holes"],,[VarInc,FCMISS][VarSet,FCMISSTXT,[StrMerge,#FCMISSTXT," Close Holes"]]]
  [If,[IExists,"Tool:SubTool:MergeDown"],,[VarInc,FCMISS][VarSet,FCMISSTXT,[StrMerge,#FCMISSTXT," MergeDown"]]]
  [If,[IExists,"Tool:Export"],,[VarInc,FCMISS][VarSet,FCMISSTXT,[StrMerge,#FCMISSTXT," Export"]]]
  [If,[IExists,"Tool:Import"],,[VarInc,FCMISS][VarSet,FCMISSTXT,[StrMerge,#FCMISSTXT," Import"]]]
]

// Returns FCRES = 1 if the run may start
[RoutineDef,FCPreflight,
  [RoutineCall,FCInitStrings]
  [VarSet,FCNL,[StrFromAsc,10]]
  [VarSet,FCHOLEPATH,[StrMerge,#FCPAL,":",#L_HOLE]]
  [VarSet,FCKEEPPATH,[StrMerge,#FCPAL,":",#L_KEEP]]
  [VarSet,FCRES,0]
  [If,([IExists,"Transform:Edit"]) && ([IGet,"Transform:Edit"]==0),
    [VarSet,FCMSG,#M_EDIT]
    [RoutineCall,FCNote]
  ,
    [RoutineCall,FCCheckButtons]
    [If,(FCMISS>0),
      [VarSet,FCMSG,[StrMerge,#M_MISS,#FCMISSTXT]]
      [RoutineCall,FCNote]
    ,
      [VarSet,FCRES,1]
      [VarSet,FCABORT,0]
      [If,(FCWARNED=0),
        [VarSet,FCWARNED,1]
        [NoteIButton,#M_YES,,,,,,,,,0xffffff,,,]
        [NoteIButton,#M_NO,,,,,,,,,0xffffff,,,]
        [VarSet,FCANS,[Note,[StrMerge,#M_FIRST1,#FCNL,#M_FIRST2,#FCNL,#M_FIRST3],,,0x1f1f1f,,640,,,,,,]]
        [If,(FCANS!=1),[VarSet,FCRES,0][VarSet,FCWARNED,0]]
      ]
    ]
  ]
]

// Export the SubTool at FCKEEPIDX alone (OBJ export writes every visible SubTool)
[RoutineDef,FCExportSolo,
  [VarSet,FCVC,[SubToolGetCount]]
  [If,(FCVC>256),[VarSet,FCVC,256]]
  [VarSet,FCI,0]
  [Loop,FCVC,
    [VarSet,FCSTAT(FCI),[SubToolGetStatus,FCI]]
    [VarInc,FCI]
  ]
  [SubToolSelect,FCKEEPIDX]
  [VarSet,FCI,0]
  [Loop,FCVC,
    [VarSet,FCST,FCSTAT(FCI)]
    [If,(FCI>=FCKEEPIDX)&&(FCI<=FCKEEPEND),
      [If,((FCST&1)=0),[SubToolSetStatus,FCI,(FCST+1)]]
    ,
      [If,((FCST&1)=1),[SubToolSetStatus,FCI,(FCST-1)]]
    ]
    [VarInc,FCI]
  ]
  [If,[IExists,"Tool:Export:QUD"],[ISet,"Tool:Export:QUD",1]]
  [If,[IExists,"Tool:Export:TRI"],[ISet,"Tool:Export:TRI",0]]
  [If,[IExists,"Tool:Export:GRP"],[ISet,"Tool:Export:GRP",1]]
  [If,[FileExists,#FCOBJ],[FileDelete,#FCOBJ]]
  [FileNameSetNext,#FCOBJ]
  [IPress,"Tool:Export"]
  [VarSet,FCI,0]
  [Loop,FCVC,
    [SubToolSetStatus,FCI,FCSTAT(FCI)]
    [VarInc,FCI]
  ]
]

// -------------------------------------------------------------- core
// Input : FCIDX (SubTool index), FCMODE (0 detect, 1 clean)
// Output: FCRES  >=0 fragment count (detect) / deleted count (clean)
//                -2 has subdivision levels, -3 split failed, -4 write-back failed
//         FCKEPT number of kept parts, FCBESTF faces of the result
[RoutineDef,FCProcess,
  [VarSet,FCRES,0]
  [VarSet,FCKEPT,1]
  [VarSet,FCBESTF,0]
  [SubToolSelect,FCIDX]
  [RoutineCall,FCGetName]
  [VarSet,FCOBJ,[StrMerge,#FCDIR,#FCNAME,".obj"]]
  [If,([IGetMax,"Tool:Geometry:SDiv"]>1),
    [VarSet,FCRES,-2]
  ,
    [If,(FCMODE=1)&&([IGet,#FCHOLEPATH]=1),
      [IPress,"Tool:Geometry:Close Holes"]
    ]
    [VarSet,FCBASE,[SubToolGetCount]]
    [IPress,"Tool:SubTool:Duplicate"]
    [If,([SubToolGetCount]!=(FCBASE+1)),
      [VarSet,FCRES,-3]
    ,
      [VarSet,FCBASE,(FCBASE+1)]
      [SubToolSelect,(FCIDX+1)]
      // Once a split has succeeded this session, "Always OK" was chosen on the
      // not-undoable note, so Enter can safely dismiss the "mesh has only one
      // part" note. Before that, Enter would hit Cancel on the confirm note.
      [If,(FCSPLITOK=1),
        [IKeyPress,13,[IPress,"Tool:SubTool:Split To Parts"]]
      ,
        [IPress,"Tool:SubTool:Split To Parts"]
      ]
      [If,([SubToolGetCount]>FCBASE),[VarSet,FCSPLITOK,1]]
      // parts occupy FCIDX+1 .. FCIDX+FCPARTS
      [VarSet,FCPARTS,([SubToolGetCount]-FCBASE+1)]
      [If,(FCPARTS<1),[VarSet,FCPARTS,1]]
      [VarSet,FCQ,((FCMODE=0)||(FCPARTS=1)||(FCPARTS>4000))]
      [If,(FCQ),
        // ---- detect only, or nothing to clean: remove all helper parts
        [VarSet,FCRES,(FCPARTS-1)]
        [If,(FCMODE=1)&&(FCPARTS>4000),[VarSet,FCRES,-3]]
        [Loop,FCPARTS,
          [If,(FCABORT=0),
            [VarSet,FCK,(FCIDX+1)]
            [RoutineCall,FCDeleteAt]
          ]
        ]
      ,
        // ---- clean: measure every part
        [VarSet,FCBEST,1]
        [VarSet,FCBESTF,-1]
        [VarSet,FCJ,1]
        [Loop,FCPARTS,
          [SubToolSelect,(FCIDX+FCJ)]
          [RoutineCall,FCFaces]
          [VarSet,FCKEEPF(FCJ),FCF]
          [If,(FCF>FCBESTF),[VarSet,FCBESTF,FCF][VarSet,FCBEST,FCJ]]
          [VarInc,FCJ]
        ]
        [VarSet,FCTHR,[IGet,#FCKEEPPATH]]
        [If,(FCTHR>100),[VarSet,FCTHR,100]]
        [If,(FCTHR<1),[VarSet,FCTHR,1]]
        // delete non-kept parts, last to first, so indices below stay valid
        [VarSet,FCKEPT,0]
        [VarSet,FCDEL,0]
        [VarSet,FCSUMF,0]
        [VarSet,FCJ,FCPARTS]
        [Loop,FCPARTS,
          [If,(FCJ=FCBEST)||((FCKEEPF(FCJ)*100)>=(FCBESTF*FCTHR)),
            [VarInc,FCKEPT]
            [VarSet,FCSUMF,(FCSUMF+FCKEEPF(FCJ))]
          ,
            [If,(FCABORT=0),
              [VarSet,FCK,(FCIDX+FCJ)]
              [RoutineCall,FCDeleteAt]
              [If,(FCABORT=0),[VarInc,FCDEL]]
            ]
          ]
          [VarDec,FCJ]
        ]
        [VarSet,FCBESTF,FCSUMF]
        // kept parts are now FCIDX+1 .. FCIDX+FCKEPT. OBJ export writes only
        // the selected SubTool, so merge them into one first.
        [If,(FCKEPT>1),
          [Loop,(FCKEPT-1),
            [If,(FCABORT=0),
              [VarSet,FCCNT,[SubToolGetCount]]
              [SubToolSelect,(FCIDX+1)]
              [IPress,"Tool:SubTool:MergeDown"]
              [If,([SubToolGetCount]=FCCNT),[VarSet,FCABORT,1]]
            ]
          ]
        ]
        [VarSet,FCKEEPIDX,(FCIDX+1)]
        [VarSet,FCKEEPEND,(FCIDX+1)]
        [If,(FCABORT=0),[RoutineCall,FCExportSolo]]
        [If,(FCABORT=0)&&[FileExists,#FCOBJ],
          [SubToolSelect,FCIDX]
          [If,[IExists,"Tool:Import:Tri2Quad"],[ISet,"Tool:Import:Tri2Quad",0]]
          [FileNameSetNext,#FCOBJ]
          [IPress,"Tool:Import"]
          [RoutineCall,FCFaces]
          [If,(FCF=FCBESTF),
            [VarSet,FCK,(FCIDX+1)]
            [RoutineCall,FCDeleteAt]
            [VarSet,FCRES,FCDEL]
          ,
            [VarSet,FCRES,-4]
          ]
          [FileDelete,#FCOBJ]
        ,
          [VarSet,FCRES,-4]
        ]
      ]
    ]
  ]
  [If,(FCABORT=1),[VarSet,FCRES,-5]]
  [SubToolSelect,FCIDX]
]

// Append one report line for the SubTool just processed
[RoutineDef,FCAddLine,
  [VarSet,FCQ,(FCIDX+1)]
  [VarSet,FCLINE,[StrMerge,FCQ,". ",#FCNAME,"  "]]
  [If,(FCRES=-2),[VarSet,FCLINE,[StrMerge,#FCLINE,#M_SDIV]]]
  [If,(FCRES=-3),[VarSet,FCLINE,[StrMerge,#FCLINE,#M_FAIL]]]
  [If,(FCRES=-4),[VarSet,FCLINE,[StrMerge,#FCLINE,#M_IMPF]]]
  [If,(FCRES=-5),[VarSet,FCLINE,[StrMerge,#FCLINE,#M_ABORT]]]
  [If,(FCRES=0),[VarSet,FCLINE,[StrMerge,#FCLINE,#M_CLEAN]]]
  [If,(FCRES>0),
    [If,(FCMODE=0),
      [VarSet,FCLINE,[StrMerge,#FCLINE,FCRES,#M_FRAG]]
    ,
      [VarSet,FCLINE,[StrMerge,#FCLINE,#M_DEL,FCRES,#M_KEPT,FCKEPT,#M_FACES,FCBESTF]]
    ]
  ]
  [If,(FCRES>0)||(FCRES<0),
    [If,(FCLISTN<100),[VarSet,FCLINES(FCLISTN),#FCLINE]]
    [VarInc,FCLISTN]
  ]
  [If,(FCRES>0),[VarInc,FCHIT][VarSet,FCSUMDEL,(FCSUMDEL+FCRES)]]
]

// Detail lines, as many per Note as fit in a ZScript string (255 bytes)
[RoutineDef,FCShowPages,
  [VarSet,FCP,0]
  [If,(FCLISTN>100),[VarSet,FCLISTN,100]]
  [Loop,100,
    [If,(FCP>=FCLISTN),[LoopExit]]
    [VarSet,FCPAGE,""]
    [Loop,12,
      [If,(FCP>=FCLISTN),[LoopExit]]
      [VarSet,FCLINE,#FCLINES(FCP)]
      [If,([StrLength,#FCPAGE]>0)&&(([StrLength,#FCPAGE]+[StrLength,#FCLINE])>225),[LoopExit]]
      [VarSet,FCPAGE,[StrMerge,#FCPAGE,#FCLINE,#FCNL]]
      [VarInc,FCP]
    ]
    [VarSet,FCMSG,#FCPAGE]
    [RoutineCall,FCNote]
  ]
]

// ---- one SubTool
[RoutineDef,FCRunCurrent,
  [RoutineCall,FCPreflight]
  [If,(FCRES=1),
    [If,([IGetMax,"Tool:Geometry:SDiv"]>1),
      [RoutineCall,FCGetName]
      [VarSet,FCMSG,[StrMerge,#M_SDV1,#FCNL,#FCNAME,#FCNL,#M_SDV3]]
      [RoutineCall,FCNote]
      [VarSet,FCRES,0]
    ]
  ]
  [If,(FCRES=1),
    [VarSet,FCIDX,[SubToolGetActiveIndex]]
    [VarSet,FCREP,""]
    [VarSet,FCLISTN,0]
    [VarSet,FCHIT,0]
    [VarSet,FCSUMDEL,0]
    [NoteBar,#M_PROG,0]
    [RoutineCall,FCProcess]
    [NoteBar,"",1]
    [RoutineCall,FCAddLine]
    [VarSet,FCMSG,[StrMerge,#M_ONE,#FCNL,#FCLINE]]
    [RoutineCall,FCNote]
  ]
]

// ---- every visible SubTool
[RoutineDef,FCRunAll,
  [RoutineCall,FCPreflight]
  [If,(FCRES=1)&&(FCMODE=1),
    [NoteIButton,#M_YES,,,,,,,,,0xffffff,,,]
    [NoteIButton,#M_NO,,,,,,,,,0xffffff,,,]
    [VarSet,FCANS,[Note,#M_ASK,,,0x1f1f1f,,560,,,,,,]]
    [If,(FCANS!=1),[VarSet,FCRES,0]]
  ]
  [If,(FCRES=1),
    [VarSet,FCORIG,[SubToolGetActiveIndex]]
    [VarSet,FCN,[SubToolGetCount]]
    [If,(FCN>256),[VarSet,FCN,256]]
    // snapshot which SubTools are visible (eye bit) before anything changes
    [VarSet,FCI,0]
    [Loop,FCN,
      [VarSet,FCVIS(FCI),([SubToolGetStatus,FCI]&1)]
      [VarInc,FCI]
    ]
    [VarSet,FCREP,""]
    [VarSet,FCLISTN,0]
    [VarSet,FCHIT,0]
    [VarSet,FCSUMDEL,0]
    [VarSet,FCTOT,0]
    [VarSet,FCVISN,0]
    [VarSet,FCI,0]
    [Loop,FCN,
      [If,(FCVIS(FCI)=1),[VarInc,FCVISN]]
      [VarInc,FCI]
    ]
    [RoutineCall,FCSdivScanAll]
  ]
  [If,(FCRES=1),
    // last to first; each SubTool's net count change is zero
    // (FCOI is used only here: the routines below reuse FCI)
    [VarSet,FCOI,(FCN-1)]
    [Loop,FCN,
      [If,(FCVIS(FCOI)=1)&&(FCABORT=0),
        [VarInc,FCTOT]
        [NoteBar,[StrMerge,#M_PROG,FCTOT,"/",FCVISN],(FCTOT/(FCVISN+1))]
        [VarSet,FCIDX,FCOI]
        [RoutineCall,FCProcess]
        [RoutineCall,FCAddLine]
      ]
      [VarDec,FCOI]
    ]
    [NoteBar,"",1]
    [If,(FCORIG<[SubToolGetCount]),[SubToolSelect,FCORIG]]
    [If,(FCMODE=0),
      [VarSet,FCMSG,[StrMerge,#M_SUM1,FCTOT,#M_SUM2,FCHIT,#M_SUM3]]
    ,
      [VarSet,FCMSG,[StrMerge,#M_SUMC1,FCTOT,#M_SUMC2,FCSUMDEL,#M_SUMC3]]
    ]
    [If,(FCLISTN>0),[VarSet,FCMSG,[StrMerge,#FCMSG,#FCNL,#M_MORE]]]
    [RoutineCall,FCNote]
    [RoutineCall,FCShowPages]
  ]
]

// -------------------------------------------------------------- UI
[VarSet,FCPAL,[StrMerge,"ZPlugin:",#L_PAL]]
[VarSet,FCB1,[StrMerge,#FCPAL,":",#L_DET1]]
[VarSet,FCB2,[StrMerge,#FCPAL,":",#L_DETA]]
[VarSet,FCB3,[StrMerge,#FCPAL,":",#L_CLN1]]
[VarSet,FCB4,[StrMerge,#FCPAL,":",#L_CLNA]]
[VarSet,FCHOLEPATH,[StrMerge,#FCPAL,":",#L_HOLE]]
[VarSet,FCKEEPPATH,[StrMerge,#FCPAL,":",#L_KEEP]]

[ISubPalette,#FCPAL]

[IButton,#FCB1,#T_DET1,
  [IShowActions,0]
  [IConfig,__ICONFIG__]
  [VarSet,FCMODE,0]
  [RoutineCall,FCRunCurrent]
,,0.5,,,]

[IButton,#FCB2,#T_DETA,
  [IShowActions,0]
  [IConfig,__ICONFIG__]
  [VarSet,FCMODE,0]
  [RoutineCall,FCRunAll]
,,0.5,,,]

[IButton,#FCB3,#T_CLN1,
  [IShowActions,0]
  [IConfig,__ICONFIG__]
  [VarSet,FCMODE,1]
  [RoutineCall,FCRunCurrent]
,,0.5,,,]

[IButton,#FCB4,#T_CLNA,
  [IShowActions,0]
  [IConfig,__ICONFIG__]
  [VarSet,FCMODE,1]
  [RoutineCall,FCRunAll]
,,0.5,,,]

[ISwitch,#FCHOLEPATH,1,#T_HOLE,,,,0.5,]
// ISlider args: name, value, resolution, min, max, info, commands,
// initially-disabled, width. A width in the disabled slot greys it out.
[ISlider,#FCKEEPPATH,10,1,1,100,#T_KEEP,,0,0.5,]
'''


def main():
    for lang in ("zh", "en"):
        for ver in ("2025", "2022"):
            d = os.path.join(HERE, "build", lang, ver)
            os.makedirs(d, exist_ok=True)
            txt = build(ver, lang).replace("__ICONFIG__", ver)
            txt.encode("ascii")  # 必须纯 ASCII
            with open(os.path.join(d, "FragClean.txt"), "w", encoding="ascii", newline="\r\n") as f:
                f.write(txt)
            print("written", lang, ver, len(txt), "bytes")


if __name__ == "__main__":
    main()
