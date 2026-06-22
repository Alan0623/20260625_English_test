#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
qs = json.load(open('/sessions/upbeat-clever-darwin/mnt/outputs/questions.json', encoding='utf-8'))

# ---- corrections (first section: 找多餘字) ----
stem_fixes = {
    '柳無蔭心柳成秧':       '柳無蔭心柳成插秧',
    '天息君行子以自強不健': '天息君行子喘以自強不健',
    '滿福氣坤滿春們乾':     '滿福氣坤滿春門乾',
    '莫死哀於大活':         '莫死哀於大心活',
}
ans_fixes = {'智義里為仁美不處仁擇得焉': 'A'}  # Q5
for q in qs:
    if q['stem'] in stem_fixes: q['stem'] = stem_fixes[q['stem']]
    if q['stem'] in ans_fixes: q['answer'] = ans_fixes[q['stem']]

# ---- 題型 → 科目分類 ----
logic_kw = ['說謊','實話','謊','推得','推論','為假','為真','必定','恆為真','何者正確',
            '何者為非','何者一定','何者恆','敘述','對面','左手邊','右手邊','隔壁','名次',
            '真話','假話','可以推得','喜歡','坐在','順序','排列','誰','前提','邏輯','圖形']
math_kw = ['元','公分','公斤','公尺','%','倍','平均','面積','周長','機率','幾','多少','除以',
           '商','餘數','平方','歲','分鐘','長度','總和','共有','售價','打折','折','除','加','減','乘']
def classify(q):
    if q['sec'] == 0:
        return '語詞類比' if any(len(v) > 1 for v in q['options'].values()) else '成語重組'
    if q['sec'] == 1: return '語詞類比'
    if q['sec'] == 2: return '詞義理解'
    if q['sec'] == 3: return '數列推理'
    if q['passage']: return '閱讀推理題組'
    s = q['stem']
    L = sum(1 for k in logic_kw if k in s); M = sum(1 for k in math_kw if k in s)
    return '邏輯推理' if (L > 0 and L >= M) else '計算應用'

ORDER = ['成語重組','語詞類比','詞義理解','數列推理','計算應用','邏輯推理','閱讀推理題組','英文基礎能力']
DESC = {
 '成語重組':'打散的成語語句中，找出多餘的字',
 '語詞類比':'A 之於 B，好像 C 之於 D 的對應關係',
 '詞義理解':'詞語、成語的意思與歸類',
 '數列推理':'數字或字母序列的規律推算',
 '計算應用':'數學與生活情境的計算題',
 '邏輯推理':'真假話、排序、條件推論等推理題',
 '閱讀推理題組':'共用題幹敘述，連續作答的推理題組',
 '英文基礎能力':'英文文法、字彙與慣用語單句選擇',
}
for q in qs:
    q['c'] = classify(q)

from collections import Counter
cnt = Counter(q['c'] for q in qs)

# ================= 每題解析 =================
# (1) 成語重組:由還原成語生成
idiom_by_num = {
 1:'前門拒虎，後門進狼',2:'明人不做暗事',3:'不知言，無以知人也',4:'上下交征利，而國危矣',
 5:'里仁為美，擇不處仁，焉得知（智）',6:'畫虎不成反類犬',7:'水能載舟，亦能覆舟',8:'無心插柳柳成蔭',
 9:'風馬牛不相及',10:'人無遠慮，必有近憂',11:'話不投機半句多',12:'出師未捷身先死',
 19:'雀屏中選',20:'無心插柳柳成蔭',21:'天行健，君子以自強不息',22:'水能載舟，亦能覆舟',
 23:'柳暗花明又一村',24:'畫虎不成反類犬',25:'天將降大任於斯人也',27:'笑問客從何處來',
 28:'秉燭夜遊',29:'大珠小珠落玉盤',30:'爆竹一聲除舊歲',31:'春滿乾坤福滿門',32:'投鼠忌器',
 33:'百步穿楊',34:'東施效顰',35:'未雨綢繆',36:'刎頸之交',37:'鞭長莫及',38:'尸位素餐',
 39:'寧為雞口，毋為牛後',40:'二桃殺三士',41:'風馬牛不相及',42:'五十步笑百步',43:'賠了夫人又折兵',
 44:'修身齊家治國平天下',45:'一日之計在於晨',46:'君子之交淡如水',47:'人生得意須盡歡',48:'一簞食，一瓢飲',
 49:'無心插柳柳成蔭',50:'船到橋頭自然直',51:'柳暗花明又一村',52:'哀莫大於心死',53:'天助自助者',
 54:'千里姻緣一線牽',55:'謠言止於智者',56:'只要勤勞，就能得到獎賞（句子）',57:'這問題確實夠嚴重了（句子）',
}
# (2) 數列:程式驗證 + 手動
import os
seq_verified = json.load(open('/sessions/upbeat-clever-darwin/mnt/outputs/seq_exp.json', encoding='utf-8')) \
               if os.path.exists('/sessions/upbeat-clever-darwin/mnt/outputs/seq_exp.json') else {}
seq_hand = {
 5:'各項是平方數，底數依序為 1、2、4、6、8、10（首項之後為偶數遞增）；故空格 = 10² = 100。',
 6:'每組是兩個連續字母「反寫」：AB→BA、CD→DC、EF→FE…；空格為 EF 反寫 = FE。',
 13:'規律交替進行「÷2」與「−4」：48÷2=24、24−4=20、20÷2=10、10−4=6、6÷2=3；故空格 = 48÷2 = 24。',
 16:'拆成兩條交錯子列：奇數位 112、□、0、−56 為等差（每次 −56），偶數位 1、2、3 遞增；故空格 = 112−56 = 56。',
 17:'拆成兩條：奇數位 16、25、36、49、64 是 4²~8²；偶數位 9、11、13、15 每次 +2；空格在偶數位 13 之後 = 15。',
 18:'這是星期一到日的英文首字母：Monday、Tuesday、Wednesday、Thursday…；空格為 Thursday = T。',
 20:'拆成兩條：奇數位 0、2、4、6、8（偶數遞增）；偶數位 1、4、9、16、□ 是 1²~5²；故空格 = 5² = 25。',
 21:'拆成兩條：偶數位 1、2、3、4、5（計數）；奇數位 1、8、□、64、125 是 1³~5³；故空格 = 3³ = 27。',
 23:'全部是立方數 0³、1³、2³、3³…= 0、1、8、27…；故空格（第一項）= 0³ = 0。',
 24:'每三項一組，形如 a、2a、4a：(1,2,4)、(2,4,8)、(□,6,12)；由 6=2a、12=4a 得 a=3，故空格 = 3。',
 25:'依序取 3、2、1 的立方、平方：3³2³1³=27,8,1；接著 3²2²1²=9,□,1；故空格 = 2² = 4。',
 26:'數列中含平方數 2²、3²、4²、5² = 4、9、16、25；空格為 3² = 9。（原題排列略有殘缺）',
 27:'每三項一組，第一項為 1、2、3，第三項為其 3 倍（3、6、9）；空格是第三組的第三項 = 3×3 = 9。',
 28:'拆成兩條：奇數位 625、576、□、484 是 25²、24²、23²、22²；偶數位 49、47、45 每次 −2；故空格 = 23² = 529。',
 31:'拆成兩條：奇數位 12、□、6、3 每次 −3；偶數位 10、12、14 每次 +2；故空格 = 12−3 = 9。',
 32:'拆成兩條：偶數位 1、3、5、7（奇數）；奇數位 29、27、23、17、□ 差為 −2、−4、−6、−8；故空格 = 17−8 = 9。',
 33:'拆成兩條：偶數位 1、2、3、4（計數）；奇數位 8、8、□、48、192 倍率為 ×1、×2、×3、×4；故空格 = 8×2 = 16。',
 34:'各項是 5 的次方，指數呈 1、−1、−2、−1、1、2 的對稱變化；故空格 = 5² = 25。',
 35:'各項是 3 的次方（3 與 1/3 互為倒數循環）；依規律空格 = 3² = 9。（原題排列略有殘缺）',
 36:'拆成兩條：奇數位 36、12、3、1 遞減，偶數位為分數列；依規律空格 = 1/3。（原題選項殘缺）',
 37:'拆成兩條：偶數位皆為 2；奇數位 72、56、□、30、20 差為 −16、−14、−12、−10；故空格 = 56−14 = 42。',
 38:'此題原檔排列疑有殘缺，規律待確認；原檔標示答案為 20。',
 42:'數列中 9、□、1 為 3²、2²、1²；故空格 = 2² = 4。',
 43:'等差數列每次 +5：1、6、11…41、(46)、51、□；故空格 = 51+5 = 56。（原檔第10項「16」應為46，為辨識誤差）',
 44:'規律為 n²+1：2、5、10、17、26、37（1²+1、2²+1…）；依此空格應為 5。原檔標示答案 7，疑有誤。',
 47:'拆成兩條：奇數位 1、3、5、7、9（奇數）；偶數位 1、9、25、49、□ 是 1²、3²、5²、7²、9²；故空格 = 9² = 81。',
 48:'每組為「XXY」其中 X、Y 為連續字母：AAB、BBC、CCD…FFG、GGH；空格 = FFG。',
 49:'字母 A、B、C…依序，數字為奇數 1、3、5…13、15；空格 = H15。',
 50:'字母 Z、Y、X…倒序；數字 0 之後為 2、4、8…倍增至 256；故空格 = 128S。',
}

def make_exp(q):
    if q['c'] == '成語重組':
        idi = idiom_by_num.get(q['num'])
        ans = q['options'].get(q['answer'], '')
        if idi:
            return f"還原後的正確語句是「{idi}」；把字按正確順序拼回後，多出來的字是「{ans}」。"
        return f"多餘的字是「{ans}」，去掉它後其餘字可重組成正確的成語／名句。"
    if q['c'] == '數列推理':
        if str(q['num']) in seq_verified: return seq_verified[str(q['num'])]
        if q['num'] in seq_hand: return seq_hand[q['num']]
    return ''  # 其餘科目分批補上

for q in qs:
    q['e'] = make_exp(q)

# ---- 索引式詳解(依題庫順序，按科目內第 N 題對應) ----
def _load(p):
    return json.load(open('/sessions/upbeat-clever-darwin/mnt/outputs/'+p, encoding='utf-8')) \
           if os.path.exists('/sessions/upbeat-clever-darwin/mnt/outputs/'+p) else {}
idx_exp = {
 '詞義理解': _load('exp_ciyi.json'),
 '語詞類比': _load('exp_leibi.json'),
 '邏輯推理': _load('exp_luoji.json'),
 '閱讀推理題組': _load('exp_yuedu.json'),
 '計算應用': _load('exp_jisuan.json'),
}
_ctr = {}
for q in qs:
    c = q['c']
    if c in idx_exp:
        _ctr[c] = _ctr.get(c, 0) + 1
        if not q['e']:
            q['e'] = idx_exp[c].get(str(_ctr[c]), '')

# ---- 併入英文科目 ----
eng = json.load(open('/sessions/upbeat-clever-darwin/mnt/outputs/eng_questions.json', encoding='utf-8'))
eng_exp = json.load(open('/sessions/upbeat-clever-darwin/mnt/outputs/eng_exp.json', encoding='utf-8'))
eng_trans = _load('eng_trans.json')
for e in eng:
    qs.append({'num': e['num'], 'sec': 99, 'passage': '', 'stem': e['stem'],
               'options': e['options'], 'answer': e['answer'], 'c': '英文基礎能力',
               'e': eng_exp.get(str(e['num']), ''), 'tr': eng_trans.get(str(e['num']), '')})

cnt = Counter(q['c'] for q in qs)  # recompute including English

# ---- 還原原本的表格(用「｜」分欄，renderStem 會渲染成表格) ----
table_fix_stem = {
 '輸入數': '若輸入數是 −10，輸出數是多少？\n輸入數｜-5｜-1｜2｜4｜9｜13\n輸出數｜-9｜-1｜5｜?｜19｜27',
 '價目表': '甲帶 500 元先買日用品花掉 300 元，再買 2 杯咖啡後剩下 100 元。下面是咖啡價目表，甲買了什麼咖啡？\n品項｜熱·大杯｜熱·小杯｜冰\n拿鐵｜55｜45｜50\n美式｜50｜40｜40',
 '煎餅': '小海貍路易斯快要 10 歲了，擔心生日派對準備不夠周全。下方表一是兩種甜點的食譜，表二是櫥櫃現有的食材：\n【表一·食譜】\n5 片煎餅｜1 份蛋糕\n麵粉 100 克｜糖 100 克\n牛奶 20 毫升｜麵粉 100 克\n雞蛋 1 顆｜奶油 100 克\n(無)｜雞蛋 2 顆\n【表二·現有食材】\n雞蛋｜6 顆\n奶油｜200 克\n糖｜500 克\n麵粉｜500 克\n牛奶｜60 毫升\n他只會完全照食譜製作、不會只做一部分。要用現有材料依食譜製作這兩種甜點，下列何者正確？',
}
table_fix_pass = {
 '贊成 反對 沒意見': '某一小學一、二、三年級共 160 人，舉辦到陽明山郊遊的表決，結果如下表：\n年級｜贊成｜反對｜沒意見\n一年級｜30｜15｜10\n二年級｜30｜15｜5\n三年級｜25｜25｜5',
}
for q in qs:
    for k, v in table_fix_stem.items():
        if k in q['stem']: q['stem'] = v
    for k, v in table_fix_pass.items():
        if q['passage'] and k in q['passage']: q['passage'] = v

data = [{'i': i+1, 'c': q['c'], 'p': q['passage'], 's': q['stem'], 'o': q['options'],
         'a': q['answer'], 'e': q['e'], 'tr': q.get('tr', '')}
        for i, q in enumerate(qs)]
payload = json.dumps(data, ensure_ascii=False)
subjects_meta = json.dumps([{'name': n, 'desc': DESC[n], 'n': cnt.get(n, 0)} for n in ORDER], ensure_ascii=False)

# ================= 各科教學 =================
LESSONS = {
 '成語重組': {
   'what':'每一題是一句被打散順序的成語或名句，並故意多塞了一個不相干的字。任務是把那個「多餘的字」找出來。',
   'tips':[
     '先別管字序，快速掃描有沒有眼熟的字組，猜出原本是哪句成語或名句。',
     '把確定的字依正確順序拼回去，剩下塞不進去的那個字，就是答案。',
     '多餘的字常與原句「音近、形近或意思相關」，用來混淆，別被牽著走。',
     '題庫多取自《論語》《孟子》、唐詩與俗諺，熟記常見名句最有幫助。',
   ],
   'ex':{'q':'風馬相不豐及牛','a':'(A) 豐',
         'why':'還原為成語「風馬牛不相及」，把字拼回去後，多出來的「豐」就是答案。'},
 },
 '語詞類比': {
   'what':'題目給「A 之於 B，好像 C 之於 D」或「A 對 B 正如 C 對 D」。先看懂 A、B 之間的關係，再選出與 C 形成「相同關係」的 D。',
   'tips':[
     '第一步：用一句話講出 A 跟 B 的關係（例如「B 是量 A 的工具」）。',
     '第二步：把同一句關係套到 C 上，看哪個選項的 D 最吻合。',
     '注意方向性：A→B 與 C→D 的先後順序要一致。',
     '兩格都空時，先鎖定最有把握的一格，再回推另一格。',
   ],
   'pat':[['種類歸屬','排球 → 球類'],['功能用途','筆 → 寫字'],['工具與對象','溫度計 → 溫度'],
          ['因果關係','努力 → 成功'],['相反相對','黑 → 白、過去 → 未來'],['部分與整體','輪胎 → 汽車'],
          ['程度深淺','涼 → 冷'],['感官對應','聲音 → 耳朵、影像 → 眼睛']],
   'ex':{'q':'聲音之於耳朵，好像影像之於＿＿','a':'(A) 眼睛',
         'why':'關係是「某種訊息對應接收它的感官器官」：聲音用耳朵接收，影像則用眼睛接收。'},
 },
 '詞義理解': {
   'what':'考詞語、成語的正確意思，或把同一類的詞歸在一起。',
   'tips':[
     '不認得整個詞時，先拆開逐字推測字義，再合起來判斷。',
     '善用上下文與詞性（動詞／名詞／形容詞）縮小範圍。',
     '用刪去法，先排除明顯相反或無關的選項。',
     '小心「望文生義」：有些成語字面與真義不同（如「危言聳聽」不是真的有危險）。',
   ],
   'ex':{'q':'「顛沛」的意思是？','a':'(D) 流離',
         'why':'「顛沛流離」形容生活困頓、四處飄泊，「顛沛」即流離失所之意。'},
 },
 '數列推理': {
   'what':'給一串數字或字母，找出排列規律，推算空缺的那一項。',
   'tips':[
     '先看相鄰兩項的「差」：差固定，就是等差數列。',
     '差不固定就看「倍數／比」：比固定，就是等比數列。',
     '對照平方數（1,4,9,16…）、立方數（1,8,27…）看看。',
     '規律很亂時，把「奇數位、偶數位」拆成兩條數列分開看（交錯數列）。',
     '字母題可用 A=1、B=2… 轉成數字，再找規律。',
   ],
   'pat':[['等差','2,4,6,8（每次 +2）'],['等比','3,9,27（每次 ×3）'],['平方數','1,4,9,16,25'],
          ['費氏相加','1,1,2,3,5,8（前兩項相加）'],['交錯數列','0,1,2,4,4,9…（奇偶位各自成列）']],
   'ex':{'q':'1，1，2，4，7，11，＿','a':'(C) 16',
         'why':'相鄰兩項的差是 0,1,2,3,4,5…，逐次加一；故下一項為 11 + 5 = 16。'},
 },
 '計算應用': {
   'what':'結合生活情境的數學題，涵蓋面積周長、比例、百分比、機率、年齡、組合等。',
   'tips':[
     '把已知條件逐一列出，設未知數、列方程式。',
     '注意單位換算（元、公分、一打 = 12…）與「第二件六折」這類折扣陷阱。',
     '「雞兔同籠」型：用頭數與腳數兩條式子聯立求解。',
     '把選項代入驗算，常能快速排除錯誤答案。',
   ],
   'pat':[['正方形','周長 = 邊長 × 4；面積 = 邊長²'],['圓','周長 = 2πr；面積 = πr²'],
          ['百分比','部分 ÷ 全體 × 100%'],['機率','符合情況數 ÷ 總情況數']],
   'ex':{'q':'屋內共 25 個頭、90 條腿，人與狗各有幾隻？','a':'人 5、狗 20',
         'why':'設人 p、狗 d。頭：p + d = 25；腿：2p + 4d = 90。聯立解得 d = 20、p = 5。'},
 },
 '邏輯推理': {
   'what':'真假話、排名順序、條件命題等推理題，重點在推論而非計算。',
   'tips':[
     '「真假話」題：假設某人說真話，往下推；若出現矛盾，就改假設。',
     '排序題：把線索畫成數線或位置圖，逐步卡位。',
     '條件命題「若 P 則 Q」等價於逆否「若非 Q 則非 P」；但不能反推成「若 Q 則 P」。',
     '「A 或 B 為假」，代表 A、B 兩者都不成立。',
   ],
   'ex':{'q':'「放了白骨精，否則我就念咒」可以推得？','a':'(C) 若不放走白骨精，就會念咒',
         'why':'這句等於「若不放，則念咒」。故能推出「不放→念咒」；但不能推出「放了就一定不念咒」。'},
 },
 '閱讀推理題組': {
   'what':'一段共用的敘述（條件）後接數個子題，需要綜合所有線索一起推理。',
   'tips':[
     '先把每條已知條件「符號化」記下來（如 甲 > 乙、孫坐李對面）。',
     '排座位、比身高時就畫圖：圓桌用圈、身高用數線，把人逐一定位。',
     '前一子題推出的結論，常能幫忙解下一子題，逐題累積資訊。',
     '善用刪去法，把不可能的選項先劃掉。',
   ],
   'ex':{'q':'乙矮於丙、高於戊；丁高於甲；丙高於甲、矮於丁。由高到矮怎麼排？','a':'丁 > 丙 > 乙 > 甲／戊',
         'why':'由「丁 > 丙 > 甲」「丙 > 乙 > 戊」串起來，先定出丁最高、丙次之、乙再次，甲與戊較矮，再依題目細分。'},
 },
 '英文基礎能力': {
   'what':'英文單句選擇題，涵蓋文法（時態、詞性、關係詞、介系詞）與字彙、慣用語。',
   'tips':[
     '先看空格前後的字，判斷需要的詞性：名詞、動詞、形容詞還是副詞。',
     '時態看時間線索：since／for → 完成式、yesterday → 過去式、will／tomorrow → 未來式。',
     '分清易混淆字組：borrow／lend、raise／rise、past／passed、except／accept。',
     '不確定時用刪去法，先排除詞性或語意明顯不合的選項。',
   ],
   'pat':[['詞性變化','danger→dangerous、convenience→convenient'],
          ['V-ing／V-ed 形容詞','exciting（形容事物）vs excited（人/動物感到）'],
          ['關係代名詞','who（人）／which（事物）／that'],
          ['介系詞','for + 時段、since + 時間點、past（經過）'],
          ['常見慣用語','get along with、pick sb up、take a seat、would rather']],
   'ex':{'q':'My dog gets ____ when he hears the doorbell ring.（A) excite (B) excited (C) exciting','a':'(B) excited',
         'why':'人或動物「感到…」用過去分詞 get excited；exciting 是用來形容令人興奮的「事物」。'},
 },
}
lessons_payload = json.dumps(LESSONS, ensure_ascii=False)

# ---- 成語教學資料(歸於「成語重組」科目) ----
idioms = [
 ["前門拒虎,後門進狼","趕走一個禍患,另一個禍患又接著到來。","俗諺(語見明代史評)","1"],
 ["明人不做暗事","光明正大的人,不會暗中做欺瞞的事。","俗諺","2"],
 ["不知言,無以知人也","不能辨識他人的言語,就無法真正了解一個人。","《論語·堯曰》","3"],
 ["上下交征利,而國危矣","上位者與下位者都競相爭奪私利,國家就危險了。","《孟子·梁惠王上》","4"],
 ["里仁為美,擇不處仁,焉得知","居住在有仁德的地方才好;選住處卻不選仁里,怎能算明智?(知=智)","《論語·里仁》","5"],
 ["畫虎不成反類犬","好高騖遠、模仿不到家,反而弄巧成拙惹人笑。","《後漢書·馬援傳》","6、24"],
 ["水能載舟,亦能覆舟","民心能擁戴君主,也能推翻君主;比喻同一力量可成事亦可敗事。","《荀子·王制》","7、22"],
 ["無心插柳柳成蔭","無意間做的事,反而意外成功。常與「有心栽花花不開」連用。","俗諺","8、20、49"],
 ["風馬牛不相及","彼此毫不相干、扯不上關係。","《左傳·僖公四年》","9、41"],
 ["人無遠慮,必有近憂","沒有長遠的考量,眼前很快就會出現憂患。","《論語·衛靈公》","10"],
 ["話不投機半句多","彼此意見不合,連半句話都嫌多餘。","俗諺","11"],
 ["出師未捷身先死","出兵還沒成功就先去世,惋惜壯志未酬。(下句:長使英雄淚滿襟)","杜甫《蜀相》","12"],
 ["雀屏中選","被選中為女婿,後泛指人才出眾而獲選。典出竇毅畫屏射雀選婿。","《舊唐書·后妃傳》","19"],
 ["天行健,君子以自強不息","天道運行剛健不止;君子應效法天,不斷奮發、永不懈怠。","《易經·乾卦·象傳》","21"],
 ["柳暗花明又一村","絕境之中忽見轉機與希望。(上句:山重水複疑無路)","陸游《遊山西村》","23、51"],
 ["天將降大任於斯人也","上天要把重大責任交付給某人。(下接:必先苦其心志…)","《孟子·告子下》","25"],
 ["笑問客從何處來","久別返鄉,孩童不識,笑著問客人從哪來;寫歲月流逝、人事已非。","賀知章《回鄉偶書》","27"],
 ["秉燭夜遊","拿著蠟燭在夜裡遊樂,比喻把握光陰、及時行樂。","李白《春夜宴從弟桃花園序》","28"],
 ["大珠小珠落玉盤","形容樂聲清脆圓潤、錯落悅耳。","白居易《琵琶行》","29"],
 ["爆竹一聲除舊歲","鞭炮響起送走舊年,迎接新春。","傳統春聯(化用王安石《元日》)","30"],
 ["春滿乾坤福滿門","春意佈滿天地、福氣盈滿門庭;常見賀年春聯。","傳統春聯","31"],
 ["投鼠忌器","想打老鼠卻怕打壞旁邊的器物;比喻有所顧忌而不敢放手去做。","《漢書·賈誼傳》","32"],
 ["百步穿楊","在百步外射穿楊葉,形容箭法或槍法極準。典出神射手養由基。","《戰國策·西周策》","33"],
 ["東施效顰","醜女東施模仿美女西施皺眉,反而更醜;比喻盲目模仿、適得其反。","《莊子·天運》","34"],
 ["未雨綢繆","趁還沒下雨先修補門窗;比喻事先做好準備。","《詩經·豳風·鴟鴞》","35"],
 ["刎頸之交","可以同生共死、患難與共的至交好友。","《史記·廉頗藺相如列傳》","36"],
 ["鞭長莫及","鞭子雖長也打不到馬腹;比喻力量達不到、顧及不了。","《左傳·宣公十五年》","37"],
 ["尸位素餐","占著職位卻不做事,白領俸祿。","《漢書·朱雲傳》","38"],
 ["寧為雞口,毋為牛後","寧願在小場面當主導,也不願在大場面任人支配。","《戰國策·韓策》","39"],
 ["二桃殺三士","用兩顆桃子引三名勇士相爭而死;比喻借刀殺人的計謀。","《晏子春秋》","40"],
 ["五十步笑百步","退五十步的人嘲笑退百步的人;比喻自己也有同樣缺點卻譏笑他人。","《孟子·梁惠王上》","42"],
 ["賠了夫人又折兵","想占便宜,結果反而雙重吃虧、損失慘重。","《三國演義》","43"],
 ["修身齊家治國平天下","先修養自身、整治家庭,進而治理國家、安定天下。","《禮記·大學》","44"],
 ["一日之計在於晨","一天的計畫要在早晨安排好;勸人把握光陰、及早規畫。","南朝·蕭繹《纂要》(後收於《增廣賢文》)","45"],
 ["君子之交淡如水","君子之間的交情清淡如水,不重利、卻長久真誠。","《莊子·山木》","46"],
 ["人生得意須盡歡","人生快意之時就該盡情歡樂,把握當下。","李白《將進酒》","47"],
 ["一簞食,一瓢飲","一竹筐飯、一瓢水;形容生活清苦卻能安貧樂道(讚顏回)。","《論語·雍也》","48"],
 ["船到橋頭自然直","事情到了關頭,自然會有解決的辦法;勸人勿過度憂慮。","俗諺","50"],
 ["哀莫大於心死","最大的悲哀,莫過於心如死灰、喪失意志與希望。","《莊子·田子方》","52"],
 ["天助自助者","上天只幫助肯自我努力的人。","勵志諺語(西諺)","53"],
 ["千里姻緣一線牽","相隔千里的男女,因緣分一線相牽而結合。典出月下老人。","俗諺(典出唐《續玄怪錄》)","54"],
 ["謠言止於智者","謠言傳到有見識的人那裡就會停止;明智者不輕信、不傳播。","《荀子·大略》","55"],
]
idiom_payload = json.dumps(idioms, ensure_ascii=False)

# ---- 英文:全民英檢中級以上單字卡(取自 320 題答案中的中級+詞彙) ----
VOCAB = [
 ["identical","[aɪˈdɛntɪkl̩]","adj.","完全相同的","14"],
 ["realization","[ˌriələˈzeʃən]","n.","領悟；實現","15"],
 ["promotion","[prəˈmoʃən]","n.","升遷；促銷","20"],
 ["portion","[ˈporʃən]","n.","部分；一份(食物)","21"],
 ["thorough","[ˈθɝo]","adj.","徹底的；周詳的","27"],
 ["digit","[ˈdɪdʒɪt]","n.","數字；位數","8"],
 ["interrupt","[ˌɪntəˈrʌpt]","v.","打斷；中斷","39"],
 ["confusing","[kənˈfjuzɪŋ]","adj.","令人困惑的","38"],
 ["curly","[ˈkɝlɪ]","adj.","捲曲的","41"],
 ["obvious","[ˈɑbvɪəs]","adj.","明顯的(obviously 顯然地)","50"],
 ["update","[ʌpˈdet]","v./n.","更新","53"],
 ["convenient","[kənˈvinjənt]","adj.","方便的","43、273"],
 ["recommend","[ˌrɛkəˈmɛnd]","v.","推薦；建議","95"],
 ["debt","[dɛt]","n.","債務","76"],
 ["succinct","[səkˈsɪŋkt]","adj.","簡潔扼要的","75"],
 ["punctual","[ˈpʌŋktʃʊəl]","adj.","準時的","80"],
 ["manufacturer","[ˌmænjəˈfæktʃərɚ]","n.","製造商","81"],
 ["prevent","[prɪˈvɛnt]","v.","預防；阻止","82"],
 ["conclude","[kənˈklud]","v.","下結論；結束","83"],
 ["essential","[ɪˈsɛnʃəl]","adj.","必要的；基本的","84"],
 ["consideration","[kənˌsɪdəˈreʃən]","n.","考慮；體貼","90"],
 ["certified","[ˈsɝtəˌfaɪd]","adj.","經認證的","91"],
 ["categorize","[ˈkætəɡəˌraɪz]","v.","將…分類","92"],
 ["superstitious","[ˌsupɚˈstɪʃəs]","adj.","迷信的","94"],
 ["negotiable","[nɪˈɡoʃɪəbl̩]","adj.","可協商的","96"],
 ["temper","[ˈtɛmpɚ]","n.","脾氣；情緒","97"],
 ["compatible","[kəmˈpætəbl̩]","adj.","相容的；合得來的","99"],
 ["assemble","[əˈsɛmbl̩]","v.","組裝；集合","101"],
 ["complicated","[ˈkɑmpləˌketɪd]","adj.","複雜的","102"],
 ["dull","[dʌl]","adj.","遲鈍的；單調無趣的","104"],
 ["qualified","[ˈkwɑləˌfaɪd]","adj.","合格的；有資格的","105"],
 ["expert","[ˈɛkspɝt]","n.","專家","111"],
 ["popularity","[ˌpɑpjəˈlærətɪ]","n.","受歡迎；普及","113"],
 ["informative","[ɪnˈfɔrmətɪv]","adj.","提供豐富資訊的","114"],
 ["dedicated","[ˈdɛdəˌketɪd]","adj.","專注的；奉獻的","115"],
 ["prior","[ˈpraɪɚ]","adj.","在先的；優先的","117"],
 ["chore","[tʃor]","n.","雜務；例行家事","120"],
 ["amazed","[əˈmezd]","adj.","感到驚奇的","121"],
 ["healthful","[ˈhɛlθfəl]","adj.","有益健康的","122"],
 ["bulky","[ˈbʌlkɪ]","adj.","笨重的；龐大的","123"],
 ["launch","[lɔntʃ]","v.","發射；推出(產品)","125"],
 ["vacancy","[ˈvekənsɪ]","n.","空缺；空房","126"],
 ["secondhand","[ˈsɛkəndˈhænd]","adj.","二手的","130"],
 ["patient","[ˈpeʃənt]","adj./n.","有耐心的；病人","140"],
 ["private","[ˈpraɪvɪt]","adj.","私人的；私密的","141"],
 ["breath","[brɛθ]","n.","呼吸；一口氣","142"],
 ["allergic","[əˈlɝdʒɪk]","adj.","過敏的","144"],
 ["unclear","[ʌnˈklɪr]","adj.","不清楚的","149"],
 ["wise","[waɪz]","adj.","有智慧的；明智的","222"],
 ["expect","[ɪkˈspɛkt]","v.","期待；預期","207"],
 ["experience","[ɪkˈspɪrɪəns]","n./v.","經驗；經歷","234"],
 ["successful","[səkˈsɛsfəl]","adj.","成功的","271"],
 ["stranger","[ˈstrendʒɚ]","n.","陌生人","272"],
 ["excuse","[ɪkˈskjuz]","n./v.","藉口；原諒","262"],
 ["pray","[pre]","v.","祈禱","286"],
 ["uniform","[ˈjunəˌfɔrm]","n.","制服","287"],
 ["scary","[ˈskɛrɪ]","adj.","嚇人的","136"],
]
vocab_payload = json.dumps(VOCAB, ensure_ascii=False)

# ================= 簡章內容 =================
info_html = '''
<div class="info">
  <div class="banner">
    <h2>國際專案管理與英文溝通實戰班</h2>
    <div class="bsub">元智大學終身教育部 ·「115 年度委託民間機構辦理商業類職業訓練－政府補助待業者免費平日班第二門（職前訓練）JB26」第 1 期</div>
    <span class="btag">政府補助 · 學費全免 · 平日班</span>
  </div>

  <div class="card"><table class="ftab"><tbody>
    <tr><td>計畫編號</td><td>1150722441</td></tr>
    <tr><td>研習期間</td><td>115.7.3 ～ 115.9.4　週一至週五　08:30 ～ 16:30</td></tr>
    <tr><td>課程時數</td><td>323 小時</td></tr>
    <tr><td>上課地點</td><td>元智大學　元智一館大樓</td></tr>
    <tr><td>招生名額</td><td>每班 30 人（報名人數無上限；甄試通過受訓最多 30 人，未達 20 人時本部保留延班或不開班之權利）</td></tr>
    <tr><td>收費標準</td><td>學員款 0 元（符合資格者政府補助，受訓完全免費）</td></tr>
    <tr><td>計畫性質</td><td>推廣教育非學分班</td></tr>
    <tr><td>計畫類別</td><td>專業技術能力</td></tr>
    <tr><td>依　　據</td><td>教育部「專科以上學校推廣教育實施辦法」辦理</td></tr>
  </tbody></table></div>

  <div class="card"><div class="sechead">課程目標</div>
    <p class="lead">0 學費、0 基礎！鎖定各產業與跨國企業的高薪 PM（專案經理）缺口！</p>
    <p>本課程實戰培訓 PMP 國際管理思維、數位自動化策略與跨國會議英文，幫你打破薪資天花板，打造企業急需的高階即戰力。
    <a href="https://reurl.cc/3bnGpl" target="_blank" rel="noopener">👉 結訓無縫接軌 104 人力銀行熱門 PM／SA 高薪職缺</a></p>
  </div>

  <div class="card"><div class="sechead">課程內容</div>
    <p>🔥 正式報名：<a href="https://its.taiwanjobs.gov.tw/Course/Detail?ID=161685" target="_blank" rel="noopener">👉 台灣就業通－本班專頁報名</a></p>
    <p class="lead">一、課程方向</p>
    <ul>
      <li><b>【首創！70 小時跨國溝通特訓】</b>專為「不敢開口」設計！全台最高時數，從遠端會議、談判協商到英文報告撰寫，徹底突破跨國專案的語言障礙。</li>
      <li><b>【PMP 國際專案管理標準】</b>非本科也能學會！導入全球通用的 PMBOK 十大知識領域與五大流程，建立專業經理人的全局思維。</li>
      <li><b>【數位轉型與自動化管理】</b>不再只做傳統行政！學會用 AI 與自動化工具拆解企業流程，撰寫工程規格書，成為帶領數位轉型的科技 PM。</li>
    </ul>
    <p class="lead">二、課程重點（專為「轉職者」與「欲晉升管理職者」設計的實戰模組）</p>
    <ol>
      <li>跨國溝通多益實戰 70hr：聚焦遠距會議、談判技巧，強化多益 TOEIC 聽讀實戰力。</li>
      <li>專案管理架構與 PMP 實務：導入全球公認 PMP 體系，結訓即具備考照時數資格。</li>
      <li>大咖重磅親授（40 年資歷上市櫃企業資深董事客座）：從成敗案例學習預算與團隊管理訣竅。</li>
      <li>數位化與自動化管理策略：學會評估「何時用 AI」，用工程師聽得懂的語言寫規格書。</li>
      <li>專案財務規劃與成本控制：看懂財報與現金流，掌握預算編製與成本效益評估。</li>
      <li>商業模式與市場經濟分析：建立商業思維，學會競爭分析與營運規劃。</li>
      <li>合約談判與風險管理：看懂合約陷阱，學習專案採購評估與風險量化模型。</li>
      <li>求職面試與履歷優化：英文面試模擬與求職信指導，助你爭取外商職缺。</li>
    </ol>
    <p class="lead">三、結訓作品與輔導證照</p>
    <ul>
      <li><b>實戰提案作品：</b>產出專屬的數位轉型專案計畫書或商業策略分析報告，面試直接秀實力。</li>
      <li><b>精準企業媒合：</b>結訓前舉辦企業媒合，鎖定 PM、系統分析（SA）、營運企劃職缺，直接對接廠商。</li>
    </ul>
  </div>

  <div class="card"><div class="sechead">師資規劃</div>
    <p>實務業界講師：40 年資歷上市櫃企業資深董事親自客座、某 AI 與區塊鏈學會理事、某金融風險評估學會理事長及常務監事、浪花科技創辦人、電子公司輔導顧問、語文教育負責人等，現職執行各種專案、語言、程式、系統等強勢業界師資，親臨授課。</p>
  </div>

  <div class="card"><div class="sechead">甄試題型</div>
    <p>本班甄試包含以下兩科（即本網站「測驗練習」的題庫來源）：</p>
    <ul>
      <li><a href="https://reurl.cc/W89M1D" target="_blank" rel="noopener">§ 英文基礎能力 §</a></li>
      <li><a href="https://lifelong.yzu.edu.tw/ESG/download/20250103-2.pdf" target="_blank" rel="noopener">§ 邏輯測驗 §</a></li>
    </ul>
  </div>

  <div class="card"><div class="sechead">報名資格（適合對象）</div>
    <ul>
      <li>正在求職或轉職、想晉升管理職、提升英文溝通與專案管理技能的待業者。</li>
      <li>欲跨足專案經理（PM）／營運企劃／商業分析師（BA）的新手或非本科轉職者。</li>
      <li>想進入跨國外商，需要強化領導與數位協作能力者。</li>
      <li>需要政府補助（學費全免）、想邊學邊領生活津貼者。</li>
    </ul>
  </div>

  <div class="card"><div class="sechead">補助與備註</div>
    <ol>
      <li>自願性失業者：補助課程費用，不補助生活津貼。</li>
      <li>特殊身份者：補助課程費用，並補助課程期間津貼，身份如下：
        <ul>
          <li>A. 非自願離職者。</li>
          <li>B. 就業服務法第 24 條第 1 項各款所列失業者：獨力負擔家計者、中高齡者、身心障礙者、原住民、低收入戶或中低收入戶中有工作能力者、長期失業者、二度就業婦女、家庭暴力被害人、更生受保護人、其他經中央主管機關認為有必要者。</li>
        </ul>
      </li>
    </ol>
    <p>津貼標準：非自願為投保薪資之六成；特定身份為政府公告最低工資之六成／月。凡曾投保勞保並具待業身份者，受訓完全免費。</p>
  </div>

  <div class="card"><div class="sechead">退費與隱私</div>
    <p><b>退費規定：</b>請參閱 <a href="https://lifelong.yzu.edu.tw/manual/Course-registration.asp#0007" target="_blank" rel="noopener">退費相關規定 &gt;&gt; 點我</a>。</p>
    <p><b>隱私權宣告：</b>報名本部學分班及政府課程，個人資料將提供予授課教授或主辦機關使用，本部不留存您繳交的個人證件，詳見 <a href="https://lifelong.yzu.edu.tw/manual-Footer-PrivacyPolicy.asp" target="_blank" rel="noopener">隱私權政策</a>。</p>
  </div>

  <div class="card"><div class="sechead">聯絡資訊</div>
    <p>元智大學終身教育部（School of Lifelong Education, Yuan Ze University）<br>
    320-315 桃園市中壢區遠東路 135 號 ｜ 電話 03-463-8800 #2490、2492 ｜ aldept@saturn.yzu.edu.tw</p>
    <p class="src">資料來源：<a href="https://lifelong.yzu.edu.tw/ListProj2_net.asp?id_pk=26184" target="_blank" rel="noopener">元智大學終身教育部－課程詳細資料</a></p>
  </div>
</div>
'''

html = '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>國際專案管理與英文溝通實戰班甄試練習題</title>
<style>
  /* Material Design 3 色彩角色(紫色種子) */
  :root{
    --bg:#eef0f4; --card:#ffffff; --ink:#1c1b20; --muted:#5a5d66;
    --line:#e4e7ec; --brand:#5b57c2; --brand2:#7a78d6; --on-primary:#ffffff;
    --ok:#146c43; --okbg:#e3f6ec; --bad:#ba1a1a; --badbg:#ffe3df;
    --soft:#ecebfb; --soft2:#f4f5f8; --txt:#2a2730;
    --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.08);
    --elev2:0 2px 4px rgba(16,24,40,.06),0 4px 12px rgba(16,24,40,.10);
  }
  body.dark{
    --bg:#141318; --card:#201f25; --ink:#e6e1e9; --muted:#cac4cf;
    --line:#48454e; --brand:#cbc2ff; --brand2:#a8a4f0; --on-primary:#2c2a78;
    --ok:#7fd9a6; --okbg:#13301f; --bad:#ffb4ab; --badbg:#3a1714;
    --soft:#3b3a66; --soft2:#2a282f; --txt:#ddd8e0;
    --shadow:0 1px 3px rgba(0,0,0,.5);
    --elev2:0 2px 6px 2px rgba(0,0,0,.5);
  }
  .tabbar{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;margin:14px 0 4px;}
  .theme-ctl{display:flex;align-items:center;gap:8px;}
  .auto-btn{min-height:44px;border:1.5px solid var(--line);background:var(--card);color:var(--muted);
    border-radius:99px;padding:0 14px;font-size:15px;font-weight:700;cursor:pointer;box-shadow:var(--shadow);}
  .auto-btn:hover{border-color:var(--brand);}
  .auto-btn.active{background:var(--brand);color:var(--on-primary);border-color:var(--brand);}
  .switch{position:relative;width:72px;height:44px;display:inline-block;cursor:pointer;flex:none;}
  .switch input{position:absolute;opacity:0;width:0;height:0;}
  .switch .track{position:absolute;top:0;left:0;width:72px;height:44px;border-radius:99px;
    background:var(--soft);border:1.5px solid var(--line);box-shadow:var(--shadow);transition:.2s;}
  .switch input:checked ~ .track{background:var(--brand);border-color:var(--brand);}
  .switch .knob{position:absolute;top:6px;left:4px;width:32px;height:32px;border-radius:50%;
    background:var(--card);color:var(--brand);display:flex;align-items:center;justify-content:center;
    box-shadow:0 1px 4px rgba(0,0,0,.35);transition:.2s;}
  .switch input:checked ~ .knob{color:var(--on-primary);}
  .switch input:checked ~ .knob{transform:translateX(32px);}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-size:16px;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif;
    line-height:1.6;}
  /* ===== Dashboard 佈局:左側選單 + 右側內容 ===== */
  .app{display:flex;min-height:100vh;}
  .sidebar{position:sticky;top:0;align-self:flex-start;height:100vh;width:260px;flex:none;
    background:var(--card);border-right:1px solid var(--line);display:flex;flex-direction:column;
    padding:14px 12px;transition:width .2s;overflow:hidden;z-index:40;}
  .sidebar.collapsed{width:76px;}
  .brand{display:flex;align-items:center;gap:10px;padding:6px 8px 14px;}
  .brand-logo{flex:none;width:36px;height:36px;border-radius:12px;background:linear-gradient(135deg,#5b57c2,#8b88e8);
    color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;}
  .brand-name{font-weight:800;font-size:18px;white-space:nowrap;}
  .sidebar.collapsed .brand-name{display:none;}
  .icon-btn{min-height:40px;width:40px;height:40px;border:1px solid var(--line);background:var(--card);
    color:var(--ink);border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;}
  .icon-btn:hover{background:var(--soft);}
  .collapse-btn{margin-left:auto;}
  .sidebar.collapsed .collapse-btn{margin:0 auto;}
  .menu{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:4px;}
  .mgroup{display:flex;flex-direction:column;}
  .mi{display:flex;align-items:center;gap:12px;padding:11px 12px;border-radius:14px;cursor:pointer;
    color:var(--ink);font-weight:700;font-size:16px;white-space:nowrap;user-select:none;}
  .mi:hover{background:var(--soft2);}
  .mi.active{background:var(--soft);color:var(--brand);}
  .mi .mi-ico{flex:none;width:22px;height:22px;display:flex;align-items:center;justify-content:center;color:inherit;}
  .mi .mi-label{flex:1;}
  .mi .mi-caret{flex:none;transition:transform .2s;color:var(--muted);}
  .mgroup.open .mi .mi-caret{transform:rotate(90deg);}
  .submenu{display:none;flex-direction:column;gap:2px;margin:2px 0 6px 0;}
  .mgroup.open .submenu{display:flex;}
  .sub{display:flex;align-items:center;gap:14px;padding:8px 12px 8px 26px;border-radius:12px;cursor:pointer;
    color:var(--muted);font-size:15px;white-space:nowrap;}
  .sub:hover{background:var(--soft2);color:var(--ink);}
  .sub.active{color:var(--brand);font-weight:700;background:var(--soft);}
  .sub .dot{width:6px;height:6px;border-radius:50%;background:currentColor;flex:none;}
  .sidebar.collapsed .mi-label,.sidebar.collapsed .mi-caret,.sidebar.collapsed .submenu{display:none;}
  .sidebar.collapsed .mi{justify-content:center;padding:11px 0;}
  .side-foot{padding:10px 6px 4px;border-top:1px solid var(--line);}
  .sidebar.collapsed .side-foot .theme-ctl{flex-direction:column;gap:8px;}
  .sidebar.collapsed .side-foot .auto-btn{padding:0;width:40px;overflow:hidden;}
  .content{flex:1;min-width:0;padding:18px 22px 80px;}
  .topbar{display:flex;align-items:center;gap:12px;margin-bottom:8px;}
  .topbar h1{margin:0;font-size:22px;letter-spacing:.3px;flex:1;}
  .hamburger{display:none;}
  .scrim{display:none;}
  @media(max-width:860px){
    .sidebar{position:fixed;left:0;top:0;transform:translateX(-100%);box-shadow:var(--elev2);}
    .sidebar.open{transform:translateX(0);}
    .sidebar.collapsed{width:260px;}
    .hamburger{display:flex;}
    .scrim.show{display:block;position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:35;}
    .content{padding:14px 14px 70px;}
  }
  header h1{margin:0;font-size:24px;letter-spacing:.5px;}
  header p{margin:6px 0 0;color:var(--muted);font-size:16px;}
  .tabs{display:flex;gap:8px;justify-content:center;}
  .tab{padding:9px 20px;border-radius:99px;border:1.5px solid var(--line);background:var(--card);
    cursor:pointer;font-weight:700;color:var(--muted);font-size:16px;
    min-height:44px;display:flex;align-items:center;}
  .tab.active{background:var(--brand);color:var(--on-primary);border-color:var(--brand);}
  .subjects{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:6px 0 4px;}
  @media(max-width:760px){ .subjects{grid-template-columns:repeat(2,1fr);} }
  @media(max-width:420px){ .subjects{grid-template-columns:1fr;} }
  .subj{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;
    cursor:pointer;transition:.18s;text-align:left;}
  .subj:hover{background:var(--soft);border-color:var(--brand2);box-shadow:var(--elev2);transform:translateY(-1px);}
  .subj .sn{font-weight:800;font-size:20px;}
  .subj .sd{font-size:16px;color:var(--muted);margin-top:2px;line-height:1.4;}
  .subj .sc{display:inline-block;margin-top:8px;font-size:16px;font-weight:700;color:var(--brand);
    background:var(--soft);border-radius:99px;padding:1px 10px;}
  .crumbs{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:4px 0 0;}
  .back{font-size:16px;color:var(--brand);cursor:pointer;font-weight:700;}
  .bar{position:sticky;top:0;z-index:20;background:var(--bg);
    backdrop-filter:blur(8px);padding:10px 0;margin:6px 0 14px;border-bottom:1px solid var(--line);}
  .progress{height:8px;background:var(--line);border-radius:99px;overflow:hidden;}
  .progress>i{display:block;height:100%;background:linear-gradient(90deg,var(--brand),var(--brand2));width:0;transition:width .3s;}
  .meta{display:flex;justify-content:space-between;align-items:center;margin-top:8px;font-size:16px;color:var(--muted);}
  .meta b{color:var(--ink);}
  .card{background:var(--card);border:1px solid var(--line);border-radius:16px;
    padding:18px 18px 14px;margin:14px 0;box-shadow:var(--shadow);}
  .passage{background:var(--soft2);border:1px dashed #c7c9f7;border-radius:12px;
    padding:10px 12px;margin:0 0 12px;font-size:16px;color:var(--txt);white-space:pre-wrap;}
  .passage::before{content:"題組說明";display:inline-block;font-size:16px;font-weight:700;
    color:var(--brand);background:var(--soft);border-radius:6px;padding:1px 7px;margin-right:8px;}
  .qnum{font-size:16px;font-weight:700;color:var(--brand);}
  .stem{font-size:16.5px;font-weight:600;margin:4px 0 12px;white-space:pre-wrap;}
  .stemrow{display:flex;gap:10px;align-items:flex-start;}
  .stemrow .stem{flex:1;margin-bottom:12px;}
  .spk{flex:none;border:1.5px solid var(--line);background:var(--card);border-radius:10px;
    padding:6px 10px;font-size:16px;line-height:1;cursor:pointer;color:var(--brand);
    display:inline-flex;align-items:center;justify-content:center;vertical-align:middle;}
  .spk:hover{border-color:var(--brand);background:var(--soft);}
  .spk.sm{padding:2px 13px;font-size:16px;margin-left:6px;}
  .opts{display:flex;flex-direction:column;gap:8px;}
  .opt{display:flex;gap:10px;align-items:center;border:1.5px solid var(--line);
    border-radius:11px;padding:10px 12px;min-height:44px;cursor:pointer;transition:.15s;background:var(--card);}
  .opt:hover{border-color:var(--brand2);background:var(--soft2);}
  .opt input{margin-top:3px;accent-color:var(--brand);}
  .opt .lbl{font-weight:700;color:var(--muted);min-width:18px;}
  .opt.sel{border-color:var(--brand);background:var(--soft);}
  .opt.correct{border-color:var(--ok);background:var(--okbg);}
  .opt.wrong{border-color:var(--bad);background:var(--badbg);}
  .opt .mark{margin-left:auto;font-weight:800;}
  .opt.correct .mark{color:var(--ok);} .opt.wrong .mark{color:var(--bad);}
  .graded .opt{cursor:default;}
  button{font:inherit;font-size:16px;min-height:44px;border:0;border-radius:22px;padding:11px 22px;cursor:pointer;font-weight:700;}
  .primary{background:var(--brand);color:var(--on-primary);} .primary:hover{background:#4338ca;}
  .ghost{background:var(--card);border:1.5px solid var(--line);color:var(--ink);} .ghost:hover{border-color:var(--brand2);}
  button:disabled{opacity:.45;cursor:not-allowed;}
  .result{margin:14px 0;padding:14px 16px;border-radius:14px;font-weight:700;text-align:center;
    background:var(--soft);color:var(--brand);display:none;}
  .result.show{display:block;}
  .nav{display:flex;justify-content:space-between;align-items:center;margin-top:18px;gap:10px;}
  select,input[type=search]{font:inherit;font-size:16px;min-height:44px;padding:8px 12px;border-radius:10px;border:1.5px solid var(--line);background:var(--card);}
  .foot{text-align:center;color:var(--muted);font-size:16px;margin-top:30px;}
  .pill{display:inline-block;background:var(--soft);color:var(--brand);border-radius:99px;
    padding:2px 10px;font-size:16px;font-weight:700;}
  /* learn / lessons */
  .lnav{display:flex;gap:8px;overflow-x:auto;padding:4px 0 8px;margin-bottom:4px;}
  .lpill{white-space:nowrap;padding:7px 16px;border-radius:99px;border:1.5px solid var(--line);
    background:var(--card);cursor:pointer;font-weight:700;font-size:16px;color:var(--muted);
    min-height:44px;display:flex;align-items:center;}
  .lpill.active{background:var(--brand);color:var(--on-primary);border-color:var(--brand);}
  .lesson h2{font-size:20px;margin:6px 0 2px;}
  .lesson .lwhat{color:var(--txt);font-size:16px;margin:6px 0 14px;}
  .sechead{font-size:16px;font-weight:800;color:var(--brand);letter-spacing:.5px;margin:0 0 8px;}
  .tips{margin:0;padding-left:20px;} .tips li{margin:6px 0;font-size:16px;}
  .ptab{width:100%;border-collapse:collapse;font-size:16px;}
  .ptab td{border:1px solid var(--line);padding:7px 10px;vertical-align:top;}
  .ptab td:first-child{font-weight:700;white-space:nowrap;background:var(--soft2);color:var(--ink);width:34%;}
  .exq{font-weight:700;font-size:16px;white-space:pre-wrap;}
  .exa{margin:8px 0;}
  .exwhy{color:var(--txt);font-size:16px;background:var(--soft2);border-left:3px solid var(--brand2);
    padding:8px 12px;border-radius:0 8px 8px 0;}
  .qexp{margin-top:10px;font-size:16px;color:var(--txt);background:var(--soft2);
    border-left:3px solid var(--brand);padding:9px 12px;border-radius:0 8px 8px 0;white-space:pre-wrap;}
  .qexp b{color:var(--brand);}
  .qexp.todo{background:#fff7ed;border-left-color:#f59e0b;color:#92400e;}
  .qexp.warn{background:#fde7ef;border-left-color:#e0567f;color:#7a1f3d;}
  body.dark .qexp.warn{background:#3a1d28;border-left-color:#f06a92;color:#f6c0d2;}
  /* 題解瀏覽 */
  .solrow{border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:10px 0;background:var(--card);}
  .solq{font-weight:700;font-size:16px;white-space:pre-wrap;}
  .solmeta{font-size:16px;color:var(--muted);margin:2px 0 6px;}
  .sola{display:inline-block;background:var(--okbg);color:var(--ok);border-radius:99px;
    padding:1px 10px;font-size:16px;font-weight:700;margin-bottom:6px;}
  .searchbox{width:100%;margin:6px 0 4px;}
  .icard{background:var(--card);border:1px solid var(--line);border-radius:14px;
    padding:13px 15px;margin:10px 0;box-shadow:var(--shadow);}
  .ihead{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;}
  .iname{font-size:18px;font-weight:800;color:var(--ink);letter-spacing:.5px;}
  .isrc{font-size:16px;color:var(--on-primary);background:var(--brand2);border-radius:99px;padding:2px 10px;font-weight:700;}
  .iq{margin-left:auto;font-size:16px;color:var(--muted);}
  .imean{margin:7px 0 0;font-size:16px;color:var(--txt);}
  .hidden{display:none;}
  .count{color:var(--muted);font-size:16px;margin:4px 0;}
  /* 單字卡 */
  .vgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:10px;}
  .vcard{border:1.5px solid var(--line);border-radius:12px;padding:11px 12px;min-height:74px;
    cursor:pointer;background:var(--card);transition:.15s;}
  .vcard:hover{border-color:var(--brand2);}
  .vcard.flip{background:var(--soft);border-color:var(--brand);}
  .vcard .vw{font-size:17px;font-weight:800;display:flex;align-items:center;gap:6px;}
  .vcard .vq{font-size:16px;color:var(--muted);margin-top:2px;}
  .vcard .vm{display:none;margin-top:7px;font-size:16px;color:var(--txt);}
  .vcard.flip .vm{display:block;}
  .vpos{font-size:16px;color:var(--brand);font-weight:700;margin-right:4px;}
  .vkk{font-size:16px;color:var(--muted);font-weight:500;}
  /* 收合區塊 */
  .acchead{font-size:16px;font-weight:800;color:var(--brand);letter-spacing:.5px;cursor:pointer;
    display:flex;justify-content:space-between;align-items:center;user-select:none;}
  .accbody{display:none;margin-top:10px;}
  .acc.open .accbody{display:block;}
  .chev{transition:transform .15s;color:var(--muted);font-size:16px;}
  .acc.open .chev{transform:rotate(90deg);}
  /* 簡章 */
  .banner{background:linear-gradient(135deg,#5b57c2,#8b88e8);color:#fff;border-radius:24px;
    padding:22px 24px;margin:6px 0 16px;box-shadow:var(--elev2);}
  .banner h2{margin:0 0 6px;font-size:21px;}
  .banner .bsub{font-size:16px;opacity:.92;line-height:1.5;}
  .banner .btag{display:inline-block;background:rgba(255,255,255,.2);border-radius:99px;
    padding:2px 12px;font-size:16px;font-weight:700;margin-top:10px;}
  .info .sechead{margin-bottom:10px;}
  .info p{margin:8px 0;font-size:16px;color:var(--txt);}
  .info ol,.info ul{margin:8px 0;padding-left:22px;} .info li{margin:6px 0;font-size:16px;}
  .info a{color:var(--brand);font-weight:700;}
  .info .lead{font-size:16px;color:var(--ink);font-weight:600;}
  .ftab{width:100%;border-collapse:collapse;font-size:16px;}
  .ftab td{border:1px solid var(--line);padding:8px 11px;vertical-align:top;}
  .ftab td:first-child{font-weight:700;background:var(--soft2);white-space:nowrap;width:30%;color:var(--ink);}
  .src{font-size:16px;color:var(--muted);margin-top:10px;}
  .ngrid{border-collapse:collapse;margin:10px 0;}
  .ngrid td{border:1.5px solid var(--line);padding:8px 16px;text-align:center;font-weight:700;
    min-width:40px;background:var(--soft2);font-size:16px;}
</style>
</head>
<body>
<div class="app">
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <span class="brand-logo">JB</span>
      <span class="brand-name">甄試練習</span>
      <button class="icon-btn collapse-btn" id="collapseBtn" title="收合／展開選單" aria-label="收合選單">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg>
      </button>
    </div>
    <nav class="menu" id="menu"></nav>
    <div class="side-foot">
      <div class="theme-ctl">
        <button id="autoBtn" class="auto-btn" title="跟隨系統深淺色">自動</button>
        <label class="switch" title="淺色／深色切換">
          <input type="checkbox" id="themeChk" aria-label="深色模式">
          <span class="track"></span><span class="knob" id="themeKnob"></span>
        </label>
      </div>
    </div>
  </aside>
  <div class="scrim" id="scrim"></div>
  <main class="content">
    <div class="topbar">
      <button class="icon-btn hamburger" id="hamburger" aria-label="開啟選單">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
      <h1>國際專案管理與英文溝通實戰班甄試練習題</h1>
    </div>

  <!-- ============ 測驗練習 ============ -->
  <div id="view-quiz">
    <div id="subjpick">
      <p style="text-align:center;color:var(--muted);font-size:16px;margin:4px 0 10px">請選擇練習科目：</p>
      <div class="subjects" id="subjects"></div>
    </div>
    <div id="practice" class="hidden">
      <div class="bar">
        <div class="crumbs">
          <span class="back" id="back">← 選擇科目</span>
          <span style="color:var(--muted)">／</span><b id="subjname"></b>
        </div>
        <div class="progress" style="margin-top:8px"><i id="pbar"></i></div>
        <div class="meta">
          <span>第 <b id="gnow"></b> / <b id="gall"></b> 組</span>
          <span>本科答對 <b id="totright">0</b> 題</span>
        </div>
        <div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:14px;justify-content:center;align-items:center">
          <span>跳至題組：<select id="gsel"></select></span>
          <span id="vpwrap"></span>
        </div>
      </div>
      <div id="quiz"></div>
      <div class="result" id="result"></div>
      <div class="nav">
        <button class="ghost" id="prev">← 上一組</button>
        <button class="primary" id="grade">提交本組批改</button>
        <button class="ghost" id="next">下一組 →</button>
      </div>
    </div>
  </div>

  <!-- ============ 科目教學 ============ -->
  <div id="view-learn" class="hidden">
    <div class="bar"><div class="lnav" id="lnav"></div></div>
    <div id="lesson" class="lesson"></div>
  </div>

  <!-- ============ 簡章 ============ -->
  <div id="view-info" class="hidden">__INFO__</div>

    <div class="foot">
      <p style="margin:0 0 6px">共 <span id="total"></span> 題 · 依題型分科 · 每 10 題一組即時批改</p>
      資料來源：使用者提供之邏輯測驗題庫 · 第 5 題答案及第 8、21、31、52 題題幹已校正
    </div>
  </main>
</div>

<script id="data" type="application/json">__DATA__</script>
<script id="subjmeta" type="application/json">__SUBJ__</script>
<script id="lessons" type="application/json">__LESSONS__</script>
<script id="idioms" type="application/json">__IDIOMS__</script>
<script id="vocab" type="application/json">__VOCAB__</script>
<script>
const QS = JSON.parse(document.getElementById('data').textContent);
const SUBJ = JSON.parse(document.getElementById('subjmeta').textContent);
const LESSONS = JSON.parse(document.getElementById('lessons').textContent);
const IDIOMS = JSON.parse(document.getElementById('idioms').textContent);
const VOCAB = JSON.parse(document.getElementById('vocab').textContent);
const PER = 10, LET = ['A','B','C','D','E','F'];
const el = id => document.getElementById(id);
const esc = t => (t||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const escAttr = t => esc(t).replace(/"/g,'&quot;').replace(/'/g,'&#39;');
const isWarn = t => /疑有誤|疑誤|存疑|有誤|疑有缺漏/.test(t||'');
// 把句中的空格填入正確答案(供英文整句發音用)
function fillBlank(stem, ans){
  ans=(ans||'').trim();
  if(/[_＿]{2,}/.test(stem)) return stem.replace(/[_＿]{2,}/, ' '+ans+' ').replace(/\\s+/g,' ').trim();
  return stem; // 無空格(原檔缺空格)則維持原句
}
// 把含「數字方格」的題幹中，整列數字渲染成表格(九宮格)
function renderStem(s){
  const lines=(s||'').split('\\n');
  const isNum=l=>{const t=l.trim().split(/\\s+/);return t.length>=2 && t.every(x=>/^[-+]?\\d+$|^[?？]$/.test(x));};
  const isCol=l=>l.indexOf('｜')>=0;
  if(!lines.some(l=>isNum(l)||isCol(l))) return esc(s);
  let out='',grid=[];
  const flush=()=>{ if(grid.length){ out+='<table class="ngrid"><tbody>'+grid.map(cells=>'<tr>'+cells.map(c=>`<td>${esc(c)}</td>`).join('')+'</tr>').join('')+'</tbody></table>'; grid=[]; } };
  lines.forEach(l=>{ if(isCol(l)) grid.push(l.split('｜').map(x=>x.trim())); else if(isNum(l)) grid.push(l.trim().split(/\\s+/)); else { flush(); if(l.trim()) out+=`<div>${esc(l)}</div>`; } });
  flush(); return out;
}
el('total').textContent = QS.length;

// ----- 深色模式：滑動開關 + 自動(跟隨系統) -----
(function(){
  const chk=el('themeChk'), autoBtn=el('autoBtn'), knob=el('themeKnob');
  const SUN='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2 12h2M20 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>';
  const MOON='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  const mq=window.matchMedia('(prefers-color-scheme: dark)');
  let mode='auto'; try{ mode=localStorage.getItem('theme')||'auto'; }catch(e){}
  const save=()=>{ try{localStorage.setItem('theme',mode);}catch(e){} };
  const effDark=()=> mode==='auto' ? mq.matches : mode==='dark';
  function render(){
    const d=effDark();
    document.body.classList.toggle('dark', d);
    chk.checked=d; knob.innerHTML=d?MOON:SUN;
    autoBtn.classList.toggle('active', mode==='auto');
  }
  chk.addEventListener('change',()=>{ mode=chk.checked?'dark':'light'; save(); render(); });
  autoBtn.addEventListener('click',()=>{ mode = (mode==='auto') ? (mq.matches?'dark':'light') : 'auto'; save(); render(); });
  mq.addEventListener('change',()=>{ if(mode==='auto') render(); });
  render();
})();

// ----- 美式英文發音(Web Speech API) -----
let _voices=[], _engVoices=[], chosenVoiceURI='';
try{ chosenVoiceURI = localStorage.getItem('ttsVoice')||''; }catch(e){}
function rankVoice(v){
  const n=(v.name||'').toLowerCase(), l=(v.lang||'').replace('_','-').toLowerCase();
  let s=0;
  if(l==='en-us') s+=40; else if(l.startsWith('en')) s+=20;
  if(n.includes('google')) s+=50;                 // Chrome 的 Google 語音(最接近 Google 翻譯)
  if(/natural|neural|premium|enhanced/.test(n)) s+=30;
  if(/samantha|ava|allison|aaron|nicky|zoe|jenny|aria|guy/.test(n)) s+=15;
  return s;
}
function loadVoices(){
  if(!('speechSynthesis' in window)) return;
  _voices=window.speechSynthesis.getVoices()||[];
  _engVoices=_voices.filter(v=>/^en/i.test((v.lang||'').replace('_','-')))
                    .sort((a,b)=>rankVoice(b)-rankVoice(a));
  document.querySelectorAll('select.voicesel').forEach(fillVoiceSel);
}
if('speechSynthesis' in window){ loadVoices(); window.speechSynthesis.onvoiceschanged=loadVoices; }
function pickVoice(){
  if(chosenVoiceURI){ const m=_voices.find(v=>v.voiceURI===chosenVoiceURI); if(m) return m; }
  return _engVoices[0] || _voices.find(v=>/en[-_]US/i.test(v.lang)) || null;
}
function speakEN(text){
  if(!('speechSynthesis' in window)){ alert('此瀏覽器不支援語音朗讀'); return; }
  const clean=(text||'').replace(/[_＿]{2,}/g,' blank ');
  const u=new SpeechSynthesisUtterance(clean);
  if(!_voices.length) loadVoices();
  const v=pickVoice();
  if(v){ u.voice=v; u.lang=v.lang; } else { u.lang='en-US'; }
  u.rate=0.95; u.pitch=1;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(u);
}
function spkIcon(sz){
  return `<svg width="${sz}" height="${sz}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7"/><path d="M19 6a9 9 0 0 1 0 12"/></svg>`;
}
function spkBtn(text, small){
  return `<button type="button" class="spk${small?' sm':''}" data-text="${escAttr(text)}" title="美式發音" aria-label="朗讀英文">${spkIcon(small?15:18)}</button>`;
}
function fillVoiceSel(sel){
  const cur=chosenVoiceURI;
  sel.innerHTML='<option value="">自動挑選最佳語音</option>'+
    _engVoices.map(v=>`<option value="${escAttr(v.voiceURI)}" ${v.voiceURI===cur?'selected':''}>${esc(v.name)}（${esc(v.lang)}）</option>`).join('');
}
function voicePicker(){
  return `<label style="font-size:16px;color:var(--muted);display:inline-flex;align-items:center;gap:6px;flex-wrap:wrap">${spkIcon(15)} 發音語音：
    <select class="voicesel"></select>
    <button type="button" class="spk sm" data-text="This is a sample of the selected voice.">試聽</button></label>`;
}
document.addEventListener('click',e=>{
  const b=e.target.closest('.spk'); if(!b) return;
  e.preventDefault(); e.stopPropagation();
  speakEN(b.getAttribute('data-text'));
});
function accCard(title, body, open){
  return `<div class="card acc${open?' open':''}"><div class="acchead">${title}<span class="chev">▸</span></div><div class="accbody">${body}</div></div>`;
}
document.addEventListener('click',e=>{
  const hd=e.target.closest('.acchead'); if(!hd) return;
  hd.parentElement.classList.toggle('open');
});
document.addEventListener('change',e=>{
  const s=e.target.closest('select.voicesel'); if(!s) return;
  chosenVoiceURI=s.value;
  try{ localStorage.setItem('ttsVoice', chosenVoiceURI); }catch(err){}
  document.querySelectorAll('select.voicesel').forEach(x=>{ if(x!==s) x.value=chosenVoiceURI; });
});

SUBJ.forEach(s=>{
  s.qs = QS.filter(q=>q.c===s.name);
  s.groups=[]; for(let i=0;i<s.qs.length;i+=PER) s.groups.push(s.qs.slice(i,i+PER));
});

let si=-1, gi=0;
const answers={}, graded={};

function renderSubjects(){
  const box=el('subjects'); box.innerHTML='';
  SUBJ.forEach((s,idx)=>{
    const d=document.createElement('div'); d.className='subj';
    d.innerHTML=`<div class="sn">${esc(s.name)}</div><div class="sd">${esc(s.desc)}</div>
      <span class="sc">${s.n} 題 · ${s.groups.length} 組</span>`;
    d.addEventListener('click',()=>{ si=idx; gi=0; showPractice(); });
    box.appendChild(d);
  });
}
function showPractice(){
  el('subjpick').classList.add('hidden'); el('practice').classList.remove('hidden');
  const s=SUBJ[si]; el('subjname').textContent=s.name; el('gsel').innerHTML='';
  s.groups.forEach((g,idx)=>{
    const o=document.createElement('option');
    o.value=idx; o.textContent=`第 ${idx+1} 組（${g[0].i}–${g[g.length-1].i} 題）`;
    el('gsel').appendChild(o);
  });
  el('gall').textContent=s.groups.length; render();
}
el('back').addEventListener('click',()=>{
  el('practice').classList.add('hidden'); el('subjpick').classList.remove('hidden'); window.scrollTo({top:0});
});
function render(){
  const s=SUBJ[si], g=s.groups[gi], key=si+'-'+gi, isG=!!graded[key];
  const quiz=el('quiz'); quiz.innerHTML=''; let lastP=null;
  g.forEach(q=>{
    const card=document.createElement('div'); card.className='card'+(isG?' graded':'');
    let h='';
    if(q.p && q.p!==lastP) h+=`<div class="passage">${renderStem(q.p)}</div>`;
    lastP=q.p||lastP;
    h+=`<div class="qnum">第 ${q.i} 題 · ${esc(q.c)}</div>`;
    if(q.c==='英文基礎能力')
      h+=`<div class="stemrow"><div class="stem">${renderStem(q.s)}</div>${spkBtn(q.s)}</div>`;
    else
      h+=`<div class="stem">${renderStem(q.s)}</div>`;
    h+='<div class="opts">';
    LET.forEach(L=>{
      if(q.o[L]===undefined) return;
      const chosen=answers[q.i]===L; let cls='opt'+(chosen?' sel':''), mk='';
      if(isG){ if(L===q.a){cls='opt correct';mk='<span class="mark">✓ 正解</span>';}
        else if(chosen){cls='opt wrong';mk='<span class="mark">✗</span>';} }
      const ospk = q.c==='英文基礎能力' ? spkBtn(q.o[L], true) : '';
      h+=`<label class="${cls}"><input type="radio" name="q${q.i}" value="${L}" ${chosen?'checked':''} ${isG?'disabled':''}>
        <span class="lbl">${L}</span><span class="txt">${esc(q.o[L])}</span>${ospk}${mk}</label>`;
    });
    h+='</div>';
    if(isG){
      if(q.e||q.tr){
        let xh=''; if(q.tr) xh+=`<div><b>翻譯：</b>${esc(q.tr)}</div>`; if(q.e) xh+=`<div><b>解析：</b>${esc(q.e)}</div>`;
        h+=`<div class="qexp${isWarn(q.e)?' warn':''}">${xh}</div>`;
      } else h+=`<div class="qexp todo">本題詳解整理中（${esc(q.c)}）</div>`;
    }
    card.innerHTML=h; quiz.appendChild(card);
  });
  quiz.querySelectorAll('input[type=radio]').forEach(r=>{
    r.addEventListener('change',e=>{
      answers[parseInt(e.target.name.slice(1))]=e.target.value;
      e.target.closest('.opts').querySelectorAll('.opt').forEach(o=>o.classList.remove('sel'));
      e.target.closest('.opt').classList.add('sel');
    });
  });
  // 英文練習顯示語音選單
  const vp=el('vpwrap');
  if(s.name==='英文基礎能力'){ if(vp.innerHTML===''){ vp.innerHTML=voicePicker(); fillVoiceSel(vp.querySelector('select.voicesel')); } }
  else vp.innerHTML='';
  el('gnow').textContent=gi+1; el('gsel').value=gi;
  el('prev').disabled=gi===0; el('next').disabled=gi===s.groups.length-1;
  el('grade').textContent=isG?'重做本組':'提交本組批改'; el('grade').className=isG?'ghost':'primary';
  const res=el('result');
  if(isG){ res.className='result show';
    res.innerHTML=`本組答對 <span class="pill">${graded[key].right} / ${g.length}</span>　·　${esc(s.name)} 累計答對 ${subjRight()} 題`;
  }else{ res.className='result'; res.innerHTML=''; }
  let done=0; s.groups.forEach((_,j)=>{ if(graded[si+'-'+j]) done++; });
  el('pbar').style.width=(done/s.groups.length*100)+'%'; el('totright').textContent=subjRight();
  window.scrollTo({top:0,behavior:'smooth'});
}
function subjRight(){ let r=0; Object.keys(graded).forEach(k=>{ if(k.startsWith(si+'-')) r+=graded[k].right; }); return r; }
el('grade').addEventListener('click',()=>{
  const key=si+'-'+gi, g=SUBJ[si].groups[gi];
  if(graded[key]){ g.forEach(q=>delete answers[q.i]); delete graded[key]; render(); return; }
  const un=g.filter(q=>!answers[q.i]).length;
  if(un>0 && !confirm(`還有 ${un} 題未作答，仍要批改嗎？`)) return;
  let right=0; g.forEach(q=>{ if(answers[q.i]===q.a) right++; }); graded[key]={right}; render();
});
el('prev').addEventListener('click',()=>{ if(gi>0){gi--;render();} });
el('next').addEventListener('click',()=>{ if(gi<SUBJ[si].groups.length-1){gi++;render();} });
el('gsel').addEventListener('change',e=>{ gi=parseInt(e.target.value); render(); });

// ----- 科目教學 -----
const LORDER = SUBJ.map(s=>s.name);
let li = 0;
function renderLnav(){
  const nav=el('lnav'); nav.innerHTML='';
  LORDER.forEach((name,idx)=>{
    const p=document.createElement('div'); p.className='lpill'+(idx===li?' active':'');
    p.textContent=name;
    p.addEventListener('click',()=>{ li=idx; renderLnav(); renderLesson(); });
    nav.appendChild(p);
  });
}
function renderLesson(){
  const name=LORDER[li], L=LESSONS[name];
  let h=`<h2>${esc(name)}</h2><div class="lwhat">${esc(L.what)}</div>`;
  if(name==='英文基礎能力') h+=`<div class="card">${voicePicker()}</div>`;
  // 解題策略(預設展開)
  let tips=''; L.tips.forEach(t=>tips+=`<li>${esc(t)}</li>`);
  h+=accCard('解題策略', `<ol class="tips">${tips}</ol>`, true);
  // 常見類型
  if(L.pat){
    let rows=''; L.pat.forEach(([a,b])=>rows+=`<tr><td>${esc(a)}</td><td>${esc(b)}</td></tr>`);
    h+=accCard('常見類型', `<table class="ptab"><tbody>${rows}</tbody></table>`, false);
  }
  // 全民英檢中級以上單字卡
  if(name==='英文基礎能力'){
    h+=accCard(`全民英檢中級以上單字卡（${VOCAB.length} 張）`,
      `<div style="font-size:16px;color:var(--muted);margin-bottom:8px">點卡片翻面看中文，按 ${spkIcon(14)} 聽發音。</div><div class="vgrid" id="vgrid"></div>`, false);
  }
  // 範例
  if(L.ex){
    h+=accCard('範例',
      `<div class="exq">${esc(L.ex.q)}</div><div class="exa"><span class="pill">答案：${esc(L.ex.a)}</span></div><div class="exwhy">${esc(L.ex.why)}</div>`, false);
  }
  // 成語表
  if(name==='成語重組'){
    h+=accCard(`成語表（前 57 題涉及，共 ${IDIOMS.length} 則）`,
      `<input type="search" id="isearch" class="searchbox" placeholder="搜尋成語、釋義或出處…（例如：莊子、柳、得意）"><div class="count" id="icount"></div><div id="ilist"></div>`, false);
  }
  // 逐題瀏覽:本科題目與詳解
  const list=QS.filter(q=>q.c===name);
  const done=list.filter(q=>q.e).length;
  h+=accCard(`本科題目與詳解（${done}/${list.length} 題已附解析）`,
    `<input type="search" id="ssearch" class="searchbox" placeholder="搜尋題目關鍵字…"><div id="sollist"></div>`, false);
  el('lesson').innerHTML=h;
  document.querySelectorAll('#lesson select.voicesel').forEach(fillVoiceSel);
  const vg=el('vgrid');
  if(vg){
    vg.innerHTML='';
    VOCAB.forEach(([w,kk,p,m,qn])=>{
      const d=document.createElement('div'); d.className='vcard';
      d.innerHTML=`<div class="vw">${esc(w)} ${spkBtn(w,true)}</div>
        <div class="vkk">${esc(kk)}</div>
        <div class="vq">題 ${esc(qn)}</div>
        <div class="vm"><span class="vpos">${esc(p)}</span>${esc(m)}</div>`;
      d.addEventListener('click',()=>d.classList.toggle('flip'));
      vg.appendChild(d);
    });
  }
  const renderSol=kw=>{
    kw=(kw||'').trim(); const box=el('sollist'); box.innerHTML='';
    list.forEach(q=>{
      if(kw && !(q.s+(q.e||'')).includes(kw)) return;
      const at=q.o[q.a]||'';
      let r=`<div class="solrow"><div class="solmeta">第 ${q.i} 題</div>`;
      if(q.p) r+=`<div class="passage">${renderStem(q.p)}</div>`;
      const qspk = q.c==='英文基礎能力' ? spkBtn(fillBlank(q.s, q.o[q.a])) : '';
      r+=`<div class="stemrow"><div class="solq">${renderStem(q.s)}</div>${qspk}</div>
        <div style="margin:6px 0"><span class="sola">答案 ${q.a}：${esc(at)}</span></div>`;
      if(q.e||q.tr){
        let xh=''; if(q.tr) xh+=`<div><b>翻譯：</b>${esc(q.tr)}</div>`; if(q.e) xh+=`<div><b>解析：</b>${esc(q.e)}</div>`;
        r+=`<div class="qexp${isWarn(q.e)?' warn':''}">${xh}</div>`;
      } else r+=`<div class="qexp todo">詳解整理中</div>`;
      r+='</div>'; box.insertAdjacentHTML('beforeend', r);
    });
  };
  el('ssearch').addEventListener('input',e=>renderSol(e.target.value));
  renderSol('');
  if(name==='成語重組'){
    el('isearch').addEventListener('input',e=>renderIdioms(e.target.value));
    renderIdioms('');
  }
  window.scrollTo({top:0});
}
function renderIdioms(kw){
  kw=(kw||'').trim(); const list=el('ilist'); if(!list) return; list.innerHTML=''; let n=0;
  IDIOMS.forEach(([name,mean,src,qn])=>{
    if(kw && !(name+mean+src).includes(kw)) return; n++;
    const c=document.createElement('div'); c.className='icard';
    c.innerHTML=`<div class="ihead"><span class="iname">${esc(name)}</span>
      <span class="isrc">${esc(src)}</span><span class="iq">題 ${esc(qn)}</span></div>
      <div class="imean">${esc(mean)}</div>`;
    list.appendChild(c);
  });
  el('icount').textContent=kw?`符合「${kw}」：${n} 則`:`共 ${IDIOMS.length} 則`;
}

// ----- 側邊主選單(可收合 / 展開子選項 / RWD 抽屜) -----
const ICONS={
 quiz:'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
 learn:'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5a2 2 0 0 1 2-2h13v15H6a2 2 0 0 0-2 2z"/><path d="M19 18H6a2 2 0 0 0-2 2"/></svg>',
 info:'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h5"/></svg>',
 caret:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>'
};
const MENU=[
 {view:'quiz', label:'測驗練習', icon:ICONS.quiz, subs:SUBJ.map((s,i)=>({label:s.name,i}))},
 {view:'learn',label:'答案解析', icon:ICONS.learn,subs:SUBJ.map((s,i)=>({label:s.name,i}))},
 {view:'info', label:'簡章',     icon:ICONS.info, subs:null},
];
let curView='quiz';
const isMobile=()=>window.matchMedia('(max-width:860px)').matches;
function closeDrawer(){ el('sidebar').classList.remove('open'); el('scrim').classList.remove('show'); }
function buildMenu(){
  const m=el('menu'); m.innerHTML='';
  MENU.forEach(g=>{
    const grp=document.createElement('div'); grp.className='mgroup'; grp.dataset.view=g.view;
    const caret=g.subs?`<span class="mi-caret">${ICONS.caret}</span>`:'';
    grp.innerHTML=`<div class="mi" data-view="${g.view}" title="${esc(g.label)}"><span class="mi-ico">${g.icon}</span><span class="mi-label">${esc(g.label)}</span>${caret}</div>`;
    if(g.subs){
      const sm=document.createElement('div'); sm.className='submenu';
      g.subs.forEach(su=>{
        const d=document.createElement('div'); d.className='sub'; d.dataset.view=g.view; d.dataset.i=su.i;
        d.innerHTML=`<span class="dot"></span><span>${esc(su.label)}</span>`;
        d.addEventListener('click',e=>{ e.stopPropagation(); pickSub(g.view,su.i); });
        sm.appendChild(d);
      });
      grp.appendChild(sm);
    }
    grp.querySelector('.mi').addEventListener('click',()=>{
      if(g.subs && !isMobile() && !el('sidebar').classList.contains('collapsed')) grp.classList.toggle('open');
      else if(g.subs) grp.classList.add('open');
      if(g.view==='quiz'){ el('subjpick').classList.remove('hidden'); el('practice').classList.add('hidden'); }
      switchView(g.view);
    });
    m.appendChild(grp);
  });
}
function setActive(){
  document.querySelectorAll('.mgroup').forEach(grp=>{
    grp.querySelector('.mi').classList.toggle('active', grp.dataset.view===curView);
  });
}
function switchView(v){
  curView=v;
  el('view-quiz').classList.toggle('hidden', v!=='quiz');
  el('view-learn').classList.toggle('hidden', v!=='learn');
  el('view-info').classList.toggle('hidden', v!=='info');
  setActive();
  if(isMobile()) closeDrawer();
  window.scrollTo({top:0});
}
function markSub(view,i){
  document.querySelectorAll('.sub').forEach(s=>s.classList.toggle('active', s.dataset.view===view && +s.dataset.i===i));
}
function pickSub(view,i){
  document.querySelectorAll('.mgroup').forEach(grp=>{ if(grp.dataset.view===view) grp.classList.add('open'); });
  if(view==='quiz'){ switchView('quiz'); si=i; gi=0; showPractice(); }
  else if(view==='learn'){ switchView('learn'); li=i; renderLnav(); renderLesson(); }
  markSub(view,i);
}
el('collapseBtn').addEventListener('click',()=>{
  if(isMobile()) closeDrawer(); else el('sidebar').classList.toggle('collapsed');
});
el('hamburger').addEventListener('click',()=>{ el('sidebar').classList.add('open'); el('scrim').classList.add('show'); });
el('scrim').addEventListener('click',closeDrawer);

buildMenu();
renderSubjects();
renderLnav();
renderLesson();
switchView('quiz');
const qg=document.querySelector('.mgroup[data-view="quiz"]'); if(qg) qg.classList.add('open');
</script>
</body>
</html>'''

html = (html.replace('__DATA__', payload).replace('__SUBJ__', subjects_meta)
            .replace('__LESSONS__', lessons_payload).replace('__IDIOMS__', idiom_payload)
            .replace('__VOCAB__', vocab_payload).replace('__INFO__', info_html))
open('/sessions/upbeat-clever-darwin/mnt/outputs/index.html','w',encoding='utf-8').write(html)
print('OK size KB:', round(len(html)/1024,1), '| lessons:', len(LESSONS), '| idioms:', len(idioms))
print('subjects:', [s for s in ORDER])
