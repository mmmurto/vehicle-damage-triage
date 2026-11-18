from pathlib import Path
from html import escape
import math, textwrap, json
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pptx import Presentation
from pptx.util import Inches as PI, Pt as PP
from pptx.dml.color import RGBColor as PC
from pptx.enum.shapes import MSO_SHAPE

ROOT=Path.cwd(); REPO=ROOT/'vehicle-damage-triage'; OUT=ROOT/'tomorrow-defence-ready';OUT.mkdir(exist_ok=True)
FONT='C:/Windows/Fonts/arial.ttf'; BOLD='C:/Windows/Fonts/arialbd.ttf'
pdfmetrics.registerFont(TTFont('Arial',FONT));pdfmetrics.registerFont(TTFont('Arial-Bold',BOLD))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
NAVY='#152B45';TEAL='#087E83';MUTED='#516479';PALE='#EFF5FA';MINT='#DDF3EF';AMBER='#FFF0D5';RED='#FBE7E8';LINE='#B9C9D8'

# Diagrams share a single set of coordinates for SVG, high-resolution PNG and PDF.
class Diagram:
 def __init__(self,w,h,title,sub):self.w=w;self.h=h;self.nodes=[];self.edges=[];self.texts=[(60,35,title,34,True,NAVY),(60,85,sub,20,False,MUTED)]
 def node(self,id,x,y,w,h,title,body='',fill=PALE):self.nodes.append(dict(id=id,x=x,y=y,w=w,h=h,title=title,body=body,fill=fill));return id
 def text(self,x,y,t,size=20,bold=False,col=MUTED):self.texts.append((x,y,t,size,bold,col))
 def edge(self,pts,label='',lx=None,ly=None,dashed=False):self.edges.append((pts,label,lx,ly,dashed))
 def lines(self,t,font,width,draw):
  out=[]
  for para in t.split('\n'):
   cur=''
   for word in para.split():
    test=(cur+' '+word).strip()
    if draw.textlength(test,font=font)>width and cur:out.append(cur);cur=word
    else:cur=test
   out.append(cur)
  return out
 def save(self,name):
  im=Image.new('RGB',(self.w,self.h),'white');dr=ImageDraw.Draw(im)
  svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}"><rect width="100%" height="100%" fill="white"/>']
  for pts,label,lx,ly,dashed in self.edges:
   dr.line(pts,fill=MUTED,width=3)
   (ax,ay),(bx,by)=pts[-2:];angle=math.atan2(by-ay,bx-ax);arr=[(bx,by),(bx-14*math.cos(angle-.45),by-14*math.sin(angle-.45)),(bx-14*math.cos(angle+.45),by-14*math.sin(angle+.45))];dr.polygon(arr,fill=MUTED)
   svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{MUTED}" stroke-width="3"'+(' stroke-dasharray="8 6"' if dashed else '')+'/>')
   svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in arr)+f'" fill="{MUTED}"/>')
   if label:self.texts.append((lx,ly,label,18,True,TEAL))
  for n in self.nodes:
   x,y,w,h=n['x'],n['y'],n['w'],n['h'];dr.rounded_rectangle((x,y,x+w,y+h),radius=18,fill=n['fill'],outline=LINE,width=2)
   svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{n["fill"]}" stroke="{LINE}" stroke-width="2"/>')
   fy=y+20
   for text,size,bold,col in [(n['title'],25,True,NAVY),(n['body'],21,False,MUTED)]:
    f=ImageFont.truetype(BOLD if bold else FONT,size)
    for ln in self.lines(text,f,w-36,dr):
     dr.text((x+18,fy),ln,font=f,fill=col);svg.append(f'<text x="{x+18}" y="{fy+size}" font-family="Arial" font-size="{size}" font-weight="'+('bold' if bold else 'normal')+f'" fill="{col}">{escape(ln)}</text>');fy+=size+8
   assert fy<=y+h+9,(n['id'],fy,y+h)
  for x,y,t,size,bold,col in self.texts:
   f=ImageFont.truetype(BOLD if bold else FONT,size);dr.text((x,y),t,font=f,fill=col);svg.append(f'<text x="{x}" y="{y+size}" font-family="Arial" font-size="{size}" font-weight="'+('bold' if bold else 'normal')+f'" fill="{col}">{escape(t)}</text>')
  svg.append('</svg>');im.save(OUT/(name+'.png'));(OUT/(name+'.svg')).write_text('\n'.join(svg),encoding='utf-8');return OUT/(name+'.png')

D=Diagram(1500,1450,'RESEARCH WORKFLOW | How the system will be built','Proposed process. Earlier data checks exist; expert labeling, model training and testing remain planned.')
D.text(60,142,'01  GET AND CHECK THE DATA',23,True,TEAL)
for id,x,tt,bb in [('rights',60,'Check permission','Record source, version and terms.\nExclude unapproved sources.'),('count',540,'Check the files','Count real images and known cars.\nFlag blur, crops and missing views.'),('dedup',1020,'Remove copies; group','Check exact and similar photos.\nKeep known car / incident groups.')]:D.node(id,x,190,420,150,tt,bb)
D.edge([(480,265),(540,265)]);D.edge([(960,265),(1020,265)])
D.text(60,390,'02  BUILD RELIABLE LABELS',23,True,TEAL)
for id,x,tt,bb in [('pilot',60,'Small review trial','Start with 36 selected images.\nExtend toward about 60 cases.'),('review',540,'Independent reviews','Two reviewers; expert review.\nRecord and discuss differences.'),('label',1020,'Create action labels','Observation / action / outcome.\nNo outcome inferred from photos.')]:D.node(id,x,440,420,150,tt,bb,MINT)
D.edge([(1230,340),(1230,365),(500,365),(500,420),(270,420),(270,440)]);D.edge([(480,515),(540,515)]);D.edge([(960,515),(1020,515)])
D.edge([(750,590),(750,625),(270,625),(270,590)],'Revise unclear rules; repeat the trial',360,602,True)
D.text(60,670,'03  FREEZE GROUPED SPLITS BEFORE TRAINING',23,True,TEAL)
for id,x,tt,bb in [('train',60,'TRAIN ~70%','Learn model weights.\nAugmentation allowed here only.'),('val',540,'VALIDATION ~15%','Choose model settings and\ninspection / concern cutoffs.'),('test',1020,'TEST ~15%','Keep hidden until settings freeze.\nIndependent source if feasible.')]:D.node(id,x,720,420,150,tt,bb)
D.edge([(1230,590),(1470,590),(1470,695),(270,695),(270,720)])
D.edge([(750,695),(750,720)]);D.edge([(1230,695),(1230,720)])
D.text(60,916,'04  COMPARE TWO PRACTICAL VERSIONS',23,True,TEAL)
D.node('base',60,968,420,160,'A. Simple baseline','Pretrained ResNet-18.\nOne photo -> three actions.',MINT)
D.node('better',540,968,420,160,'B. Evidence-based version','Damage detector + action rules.\nCombine views only if linked.',MINT)
D.node('lock',1020,968,420,160,'Choose, then freeze','Use validation only.\nSave model, cutoffs and code ID.',AMBER)
D.edge([(270,870),(270,895),(40,895),(40,950),(270,950),(270,968)])
D.edge([(40,950),(750,950),(750,968)])
D.edge([(750,870),(750,915),(1230,915),(1230,968)])
D.edge([(480,1080),(495,1080),(495,1170),(1120,1170),(1120,1128)])
D.edge([(960,1048),(1020,1048)])
D.node('final',60,1235,1380,130,'05  TEST ONCE; EXPLAIN THE RESULTS','Report serious-to-low-concern errors, three-class results and inspection rate.\nReview hard cases. Save logs and write the report. No tuning on the final test.',PALE)
D.edge([(1320,1128),(1320,1235)]);D.edge([(1440,795),(1480,795),(1480,1300),(1440,1300)],'Test only after freeze',1130,1186)
D.text(60,1403,'If grouping or expert review is unavailable, state the limitation and narrow the claim. Never invent either.',18)
research=D.save('01_Research_Workflow')

F=Diagram(1500,1660,'SYSTEM WORKFLOW | How one car will be checked','Proposed decision process. Clear visible danger takes priority over missing views.')
F.node('input',460,150,580,100,'1. Add photos of one car','Keep view names and case ID if available.')
F.node('valid',460,300,580,120,'2. Are any photos usable?','Decode files; check blur, light and framing.')
F.node('retake',60,300,310,135,'Unusable photos','Inspection required.\nRequest clearer views.',AMBER)
F.edge([(750,250),(750,300)]);F.edge([(460,355),(370,355)],'No',395,323)
F.node('find',460,475,580,125,'3. Find visible damage','Locate findings; record part, view and uncertainty.')
F.edge([(750,420),(750,475)],'Yes',770,434)
F.node('hazard',460,660,580,110,'4. Clear serious visible hazard?','Example: shredded tire or displaced wheel.')
F.edge([(750,600),(750,660)])
F.node('stop',1120,640,325,160,'DO NOT DRIVE','Name the finding.\nProfessional assessment\nbefore driving.',RED)
F.edge([(1040,715),(1120,715)],'Yes',1060,679)
F.node('coverage',460,835,580,110,'5. Enough views and no unresolved issue?','Check impact context, glass and nearby wheels.')
F.edge([(750,770),(750,835)],'No',770,787)
F.node('inspect',60,820,310,155,'INSPECTION REQUIRED','Explain what is missing\nor cannot be checked.',AMBER)
F.edge([(460,890),(370,890)],'No / unsure',365,852)
F.node('cosmetic',460,1010,580,110,'6. Only small cosmetic or no visible damage?','Use the full submitted evidence; do not guess.')
F.edge([(750,945),(750,1010)],'Yes',770,960)
F.edge([(460,1065),(400,1065),(400,975),(215,975)],'No / unsure',85,1005)
F.node('low',460,1180,580,135,'LOW VISIBLE CONCERN','Describe the finding accurately.\nRoadworthiness was not verified.',MINT)
F.edge([(750,1120),(750,1180)],'Yes',770,1136)
F.node('report',60,1400,1385,150,'7. Show category + visible reason + next step','Use only evidence visible in the submitted photos. Save findings and missing-view flags.\nOptional spoken summary reads the same answer. Never claim brakes, steering or engine work.',PALE)
F.edge([(750,1315),(750,1400)])
F.edge([(1282,800),(1470,800),(1470,1475),(1445,1475)])
F.edge([(215,975),(30,975),(30,1475),(60,1475)])
F.edge([(215,435),(20,435),(20,1370),(215,1370),(215,1400)])
F.text(60,1595,'Glass: location + extent + effect on driver view. Uncertain liquid is not proof of a particular fluid leak.',19)
inference=F.save('02_System_Workflow')

refs=[
'[1] X. Wang, W. Li and Z. Wu, “CarDD: A New Dataset for Vision-Based Car Damage Detection,” IEEE Transactions on Intelligent Transportation Systems, 24(7), 7202–7214, 2023. DOI: 10.1109/TITS.2023.3258480.',
'[2] V.-D. Hoang, N. T. Huynh, N. Tran, K. Le, T.-M.-C. Le, A. Selamat and H. D. Nguyen, “Powering AI-driven car damage identification based on VeHIDE dataset,” Journal of Information and Telecommunication, 9(1), 24–43, 2025; online 25 June 2024. DOI: 10.1080/24751839.2024.2367387.',
'[3] K. He, X. Zhang, S. Ren and J. Sun, “Deep Residual Learning for Image Recognition,” CVPR, 770–778, 2016. https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html',
'[4] C. Guo, G. Pleiss, Y. Sun and K. Q. Weinberger, “On Calibration of Modern Neural Networks,” ICML, PMLR 70, 1321–1330, 2017. https://proceedings.mlr.press/v70/guo17a.html',
'[5] Y. Geifman and R. El-Yaniv, “Selective Classification for Deep Neural Networks,” Advances in Neural Information Processing Systems 30, 2017. https://proceedings.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html',
'[6] CarDD dataset license. https://cardd-ustc.github.io/docs/CarDD_license.pdf. Prior consent for research and authorization for redistribution are required.',
'[7] Project archive audit, commit 3482f30, docs/07_vehide_audit.md. https://github.com/mmmurto/vehicle-damage-triage/blob/3482f30/docs/07_vehide_audit.md. Internal recorded audit, not independently repeated for this proposal.',
'[8] Project pilot sample, commit 3482f30, pilot/04_pilot_report.md. https://github.com/mmmurto/vehicle-damage-triage/blob/3482f30/pilot/04_pilot_report.md. Sample built; expert action labels remain open.',
'[9] DrBimmer/comprehensive-car-damage, Hugging Face dataset card. https://huggingface.co/datasets/DrBimmer/comprehensive-car-damage. Earlier project audit: 2,300 rows, revision 355b0990; upstream photograph rights require review.'
]
# Each page is content shared by the Word and PDF versions.
pages=[]
def page(title):p={'title':title,'blocks':[]};pages.append(p);return p['blocks']
def para(b,t):b.append(('p',t))
def head(b,t):b.append(('h',t))
def table(b,headers,rows):b.append(('table',(headers,rows)))
def image(b,path,width,height,cap):b.append(('image',(str(path),width,height,cap)))

b=page('Bachelor Dissertation Proposal')
para(b,'Working title: Vehicle Damage Assessment from Images for Driveability Triage')
para(b,'Plain-English meaning: using car photos to explain visible damage and suggest the next step.')
table(b,['Student details','Complete before printing'],[['Name / Student number','________________ / ________________'],['University / Programme','________________ / ________________'],['Supervisor / Proposal date','________________ / ________________']])
head(b,'1. Background and purpose | 题目背景和意义')
para(b,'Photos are useful for showing damage after an accident, but not all damage has the same meaning. A shallow scratch may mainly affect appearance. A shredded tire or a wheel moved out of place is a clear reason for professional assessment before driving. Other cases are unclear because the photos are poor or do not show the affected area well enough.')
para(b,'This project will build and test a computer vision system for passenger cars. It will identify visible findings and recommend one of three next steps. It is a first visual check, not a full vehicle inspection. It must not infer that the brakes, steering or engine work correctly from appearance.')
head(b,'Aim')
para(b,'Find out how well a model can separate small visible cosmetic damage, clear serious visible hazards, and cases that need inspection. Every answer will include the category, the visible reason and the next step.')
head(b,'Why this is useful')
para(b,'The study can support clearer early advice to a driver or reviewer. Its main value is to reduce false reassurance, explain missing evidence and measure when photo-based assessment is not enough. It will not certify legal roadworthiness or replace a qualified mechanic.')
para(b,'Proposal status: data checks and a sample exist. Expert labeling, model training and final model testing have not been completed. The official title and student details must be confirmed before submission.')

b=page('Research basis and questions')
head(b,'2. Related work | 国内外研究现状')
para(b,'CarDD provides 4,000 damage photographs with boxes and masks for six damage types [1]. VehiDE supports damage recognition and localization using a larger set of photographs [2]. These resources help a model learn what visible damage looks like. Their damage labels do not, by themselves, establish whether a car passed a hands-on safety inspection.')
para(b,'ResNet offers a well-established image-recognition backbone for a manageable first model [3]. Confidence scores need care: a high score is not proof that an answer is correct [4]. Work on selective classification studies when a model should avoid a firm decision [5]. This project will test that idea alongside a meaningful inspection category; it will not treat all inspection cases as the same kind of uncertainty.')
head(b,'Research questions')
para(b,'RQ1. How well does a simple image model agree with expert-reviewed visual triage labels for the three actions?')
para(b,'RQ2. Does a damage-localization model with clear action rules reduce serious visual cases given a low-concern answer? Where linked views exist, does combining them help?')
para(b,'RQ3. How does sending more cases for inspection affect missed serious findings and useful low-concern decisions, especially for glass, tires/wheels, possible leaks and poor views?')
head(b,'3. Main content | 主要内容与待解决的问题')
table(b,['Output category','Meaning and action'],[['Low visible concern','Enough clear views for the limited visual check; only cosmetic or no visible damage. Say: “Roadworthiness was not verified.”'],['Do not drive','Clear serious visible evidence, such as a shredded tire or impact-displaced wheel. Name the finding and seek professional assessment before driving.'],['Inspection required','Unclear or incomplete views, or a safety-related issue the photos cannot resolve. Explain what needs a closer or hands-on check.']])
para(b,'Glass is assessed by location, severity and effect on the driver’s view. “Broken glass” alone is not an action label. Uncertain liquid should not be identified as fuel, brake fluid or harmless water from color alone.')

b=page('Data and labeling plan')
head(b,'4. Methods and implementation | 设计方法与实施方案')
head(b,'4.1 Data already recorded and possible additions')
table(b,['Source','Count and present status','Use / limitation'],[['VehiDE','13,945 files; 36,081 regions; 7 classes in earlier archive audit [7].','Recorded prior audit, not re-run here. Paper reports 8 classes [2]; discrepancy retained. No tire/wheel/fluid class in audited labels.'],['DrBimmer','Earlier audit: 2,300 rows [9]. 36-image sample selected [8].','Front/rear normal, crushed and breakage labels. These are not confirmed safety outcomes.'],['CarDD','4,000 images reported by authors [1].','Useful damage types including tire flat. Original permission is required [6]. Not counted as newly secured.'],['Other licensed sources','Candidate counts and rights still under review.','Add diverse hazards only after rights, provenance and overlap checks. Do not add mirror counts together.']])
para(b,'The collection goal is more than 20,000 usable real unique images, with 50,000+ a stretch goal if access and useful coverage allow. This is not a completed count or a guaranteed minimum for model success. Learning curves will show whether additional data helps. Count known vehicles or incidents separately from photographs; unknown identity stays unknown.')
head(b,'4.2 Review pilot and separate label layers')
para(b,'Start with the existing 36-image sample and extend toward about 60 cases, adding serious and borderline findings. Two reviewers will label independently; a qualified automotive assessor should review disagreements. Record original votes and agreement before settling differences. Do not call student-only judgments expert review.')
para(b,'Keep three fields separate: (A) visible observation and supporting view; (B) recommended visual action and reason; (C) verified inspection result, only when a legitimately linked record exists. No reviewed source has yet been verified to provide adequate linked functional roadworthiness outcomes. If none becomes available, evaluate expert visual triage only.')
para(b,'Remove exact and near-duplicates across sources before splitting. Keep known or carefully reviewed vehicle/incident groups together. Timestamp similarity is only a clue, not proof of the same car. Retain grouping confidence. Exclude or quarantine unresolved overlaps rather than claiming an independent test.')

b=page('Research workflow and model comparison')
head(b,'4.3 Planned research workflow')
image(b,research,6.75,6.525,'Figure 1. Detailed research workflow. Ratios are provisional; the final test stays separate. All model and expert-labeling stages are planned.')
para(b,'Baseline: fine-tune a pretrained ResNet-18 image classifier with three action outputs. Improvement: use a compact damage detector, trained on permitted boxes or masks, then combine findings with documented action rules and view/quality checks. A YOLO-family detector is a practical candidate; its exact version, weights and license will be recorded before use. Multi-view pooling is conditional on reliable links between photographs.')
para(b,'Damage-recognition labels and triage labels are not interchangeable. Detection training may use more images than the expert-reviewed triage subset. Comparisons will use the same eligible test cases. Record code commit, manifests, weights, seeds, settings and hardware. Hardware availability determines final training size, not an invented completed implementation.')

b=page('System workflow and safety decisions')
head(b,'4.4 Planned workflow for one submitted car')
image(b,inference,6.5,7.193,'Figure 2. Decision workflow. A clear hazard is not downgraded because other views are missing. Low concern is not a safety certificate.')
para(b,'Outputs use a controlled template: category, observed finding and next step. Missing views and unresolved concerns are stated. Optional text-to-speech reads the same short summary. No chatbot is allowed to invent damage or mechanical function. If a clear finding cannot be resolved, inspection remains the appropriate route.')

b=page('Evaluation and expected results')
head(b,'4.5 Fair testing')
para(b,'Create grouped training, validation and test sets, provisionally around 70/15/15, after deduplication. Train on the first set, select settings and cutoffs using validation only, and freeze the method before opening the final test. Reserve a different original source for a separate test where possible, after checking overlap. If vehicle grouping is unavailable, report image-level results with that limitation.')
head(b,'Primary mistake')
para(b,'Count cases where the expert visual reference is “do not drive” but the model predicts “low visible concern.” Divide by all expert “do not drive” reference cases. Report the numerator and denominator, not only a percentage. If there are no such reference cases, the rate is undefined. Do not describe this as a measured actual-unsafe error without adequate inspection-backed outcomes.')
head(b,'Other checks')
para(b,'Report per-class precision and recall, a three-by-three confusion matrix, inspection-referral rate, and the share of low-concern answers that conflict with serious references. Explain uncertainty with intervals and class counts. Compare against an all-inspection rule: sending every case to inspection cannot count as useful success. Plot the trade-off between missed serious cases, referral rate and useful low-concern coverage.')
para(b,'Inspect failures involving poor light, blur, missing angles, glass location/visibility, tires/wheels and possible leakage. Use vehicle/incident-level confidence intervals where grouping supports them; otherwise explain image dependence. Use training subsets for learning curves while leaving the evaluation sets fixed.')
head(b,'Performance targets and limits')
para(b,'Set numerical targets only after the pilot establishes measurable class coverage and review quality, and before final testing. No accuracy or safety-error rate is promised. A result showing that photographs are insufficient is still a valid research finding. Without qualified assessors or inspection records, narrow the claim and report the resulting reference-label limits.')
head(b,'Expected deliverables')
para(b,'A documented source and rights inventory; a versioned labeling guide; a reproducible baseline and one tested improvement; a small photo-upload prototype; saved experiment logs and error analysis; and a planned 70-page dissertation. The expected contribution is an evidence-based visual-triage evaluation, not a new roadworthiness standard or a claimed novel neural architecture.')

b=page('Schedule, resources and risks')
head(b,'5. Work schedule | 进度计划')
para(b,'Provisional eight-week sequence after proposal approval. Replace it with the supervisor’s approved dates; no university deadline has been verified. This schedule is a planning estimate, not a promise to obtain 50,000 images or complete expert review in that time.')
table(b,['Stage','Planned work and completion evidence'],[['Week 1','Confirm scope, ethics/consent needs, available GPU and dataset rights. Save source/version records.'],['Weeks 2–3','Reproduce data audit, check duplicates and grouping, run the labeling pilot, recruit qualified review and revise the guide.'],['Weeks 3–4','Expand permitted data and expert-reviewed subset as feasible. Freeze split manifests and numerical evaluation criteria.'],['Weeks 4–5','Train baseline; record settings and learning curves. Start the localization-plus-rules comparison.'],['Week 6','Select settings on validation only; freeze the selected model and policy.'],['Week 7','Run held-out and independent-source testing; review errors and uncertainty.'],['Week 8','Complete the report, reproducibility checks, prototype demonstration and defence preparation.']])
head(b,'Resources and practical fallback')
para(b,'Planned tools: Python, PyTorch/torchvision, image-processing libraries and a lightweight upload interface. Use a suitable local or university/cloud GPU if available; keep the first model small. A smaller licensed dataset with trustworthy labels is preferable to an unverified large merge. Expert review remains a separate staffing requirement, not a software feature.')
para(b,'If multi-view links cannot be verified, compare image-level models and state the limit. If serious hazards are too rare, collect targeted permitted examples or narrow the question; do not claim three-class reliability from a missing class. Keep synthetic/augmented counts separate and exclude them from final test sets.')
head(b,'Data protection and reporting')
para(b,'Check ethics and data-use rules before collecting workshop records or recruiting reviewers. Avoid public plates, faces, personal inspection reports and credentials. Commit code, documentation, permitted metadata and aggregate results to GitHub; do not upload restricted photographs. Save every experiment’s data version and code ID so results can be checked.')

b=page('References and final scope statement')
head(b,'References')
for r in refs:para(b,r)
head(b,'What this proposal does and does not claim')
para(b,'Completed preparation: existing research files, a recorded VehiDE audit and a selected 36-image trial sample. Not completed: expert action labels and agreement, model training, comparative experiments or final test results. The 13,945 figure is not a final deduplicated unique-vehicle count.')
para(b,'The study will evaluate agreement with qualified visual reviewers unless adequate linked inspection evidence becomes available. Damage type, repair cost, salvage status and a vehicle’s appearance do not by themselves establish brake, steering or engine function. Actual roadworthiness remains outside what photographs alone can verify.')
para(b,'Format note: sections follow the supplied Chinese opening-report example: background/significance; related work; main content/problems; method/implementation; schedule; references. This is an English proposal, not an officially verified university form. Confirm the approved title, student details and any required Chinese-language or signed form before submission.')

styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyA',fontName='Arial',fontSize=10.4,leading=14.2,spaceAfter=8,textColor=colors.HexColor(NAVY)));styles.add(ParagraphStyle(name='HeadA',fontName='Arial-Bold',fontSize=12.7,leading=16,spaceAfter=8,spaceBefore=7,textColor=colors.HexColor(TEAL)));styles.add(ParagraphStyle(name='TitleA',fontName='Arial-Bold',fontSize=20,leading=25,spaceAfter=14,textColor=colors.HexColor(NAVY)));styles.add(ParagraphStyle(name='SmallA',fontName='Arial',fontSize=8.8,leading=11.8,spaceAfter=7,textColor=colors.HexColor(MUTED)))
styles.add(ParagraphStyle(name='CellA',fontName='Arial',fontSize=8.7,leading=11.5,textColor=colors.HexColor(NAVY)));styles.add(ParagraphStyle(name='CellH',parent=styles['CellA'],fontName='Arial-Bold',textColor=colors.white))
# PDF uses English headings; bilingual labels remain in DOCX for template traceability.
def en(t):return t.split(' | ')[0] if ' | ' in t else t

def pdf_footer(c,doc):
 c.setStrokeColor(colors.HexColor(LINE));c.line(42,33,A4[0]-42,33);c.setFont('Arial',8);c.setFillColor(colors.HexColor(MUTED));c.drawString(43,22,'VEHICLE DAMAGE ASSESSMENT | PROPOSAL');c.drawRightString(A4[0]-43,22,f'{doc.page}')

def build_pdf(path,pages):
 story=[]
 for i,p in enumerate(pages):
  if i:story.append(PageBreak())
  story.append(Paragraph(escape(p['title']),styles['TitleA']))
  for typ,dat in p['blocks']:
   if typ=='p':story.append(Paragraph(escape(dat),styles['BodyA'] if i!=7 else styles['SmallA']))
   elif typ=='h':story.append(Paragraph(escape(en(dat)),styles['HeadA']))
   elif typ=='table':
    hs,rows=dat;n=len(hs);widths=([155,356] if n==2 else [97,208,206]);values=[[Paragraph(escape(str(c)),styles['CellH'] if j==0 else styles['CellA']) for c in rr] for j,rr in enumerate([hs]+rows)]
    t=Table(values,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(NAVY)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor(PALE)]),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor(LINE))]));story.extend([t,Spacer(1,10)])
   elif typ=='image':
    fn,w,h,cap=dat;story.extend([RLImage(fn,w*72,h*72),Spacer(1,5),Paragraph(escape(cap),styles['SmallA'])])
 doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=39,bottomMargin=44,title='Vehicle Damage Assessment - Dissertation Proposal',author='Student details to be completed');doc.build(story,onFirstPage=pdf_footer,onLaterPages=pdf_footer)

proposal_pdf=OUT/'PRINT_Proposal.pdf';build_pdf(proposal_pdf,pages)

def doc_setup(title):
 d=Document();s=d.sections[0];s.page_width=Inches(8.2677);s.page_height=Inches(11.6929);s.left_margin=Inches(.58);s.right_margin=Inches(.58);s.top_margin=Inches(.55);s.bottom_margin=Inches(.55)
 st=d.styles['Normal'];st.font.name='Arial';st.font.size=Pt(10);st.paragraph_format.space_after=Pt(6);st.paragraph_format.line_spacing=1.08
 for k in ['Title','Heading 1','Heading 2']:d.styles[k].font.name='Arial';d.styles[k].font.color.rgb=RGBColor.from_string(NAVY[1:])
 d.styles['Heading 1'].font.size=Pt(19);d.styles['Heading 2'].font.size=Pt(12)
 s.header.paragraphs[0].text=title;s.header.paragraphs[0].style='Caption';p=s.footer.paragraphs[0];p.text='Vehicle damage project | ';f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');p._p.append(f);return d

def build_doc(d,pages):
 for i,p in enumerate(pages):
  if i:d.add_page_break()
  d.add_heading(p['title'],1)
  for typ,dat in p['blocks']:
   if typ=='p':d.add_paragraph(dat)
   elif typ=='h':d.add_heading(dat,2)
   elif typ=='table':
    hs,rows=dat;t=d.add_table(rows=1,cols=len(hs));t.style='Light Shading Accent 1'
    for c,v in zip(t.rows[0].cells,hs):c.text=v
    for rr in rows:
     for c,v in zip(t.add_row().cells,rr):c.text=v
    for row in t.rows:
     trpr=row._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
     for cell in row.cells:
      for paraa in cell.paragraphs:
       for r in paraa.runs:r.font.size=Pt(8.7)
   elif typ=='image':
    fn,w,h,cap=dat;d.add_picture(fn,width=Inches(w));d.add_paragraph(cap,'Caption')
 return d
proposal_doc=OUT/'Proposal_Editable.docx'
with proposal_doc.open('xb') as f:build_doc(doc_setup('BACHELOR DISSERTATION | OPENING PROPOSAL'),pages).save(f)
# Standalone vector-friendly workflow PDF (draw original SVG through svglib).
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
wf=OUT/'Workflow_Diagrams.pdf';c=canvas.Canvas(str(wf),pagesize=A4)
for nm in ['01_Research_Workflow','02_System_Workflow']:
 drawing=svg2rlg(str(OUT/(nm+'.svg')));scale=min((A4[0]-36)/drawing.width,(A4[1]-36)/drawing.height);drawing.scale(scale,scale);renderPDF.draw(drawing,c,18,A4[1]-18-drawing.height*scale);c.showPage()
c.save()

# Seven concise main slides; two detailed diagrams are question-only backups.
P=Presentation();P.slide_width=PI(13.333);P.slide_height=PI(7.5)
def t(sl,x,y,w,h,words,size=24,col=NAVY,bold=False):
 sh=sl.shapes.add_textbox(PI(x),PI(y),PI(w),PI(h));tf=sh.text_frame;tf.word_wrap=True;tf.margin_left=0;tf.margin_right=0;tf.margin_top=0;tf.margin_bottom=0
 # Estimate line fit using the same Arial metrics; never claim this replaces PowerPoint rendering.
 face='Arial-Bold' if bold else 'Arial'
 original=size
 while size>min(original,14):
  total=0
  for line_text in words.split('\n'):
   used=0;lines=1
   for word in line_text.split():
    word_width=pdfmetrics.stringWidth(word+' ',face,size)
    if used+word_width>w*72 and used:lines+=1;used=0
    used+=word_width
   total+=lines
  if total*size*1.17<=h*72:break
  size-=1
 for i,ln in enumerate(words.split('\n')):
  pp=tf.paragraphs[0] if not i else tf.add_paragraph();pp.text=ln;pp.font.name='Arial';pp.font.size=PP(size);pp.font.bold=bold;pp.font.color.rgb=PC.from_string(col.lstrip('#'))
 return sh

def bx(sl,x,y,w,h,fill):
 sh=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,PI(x),PI(y),PI(w),PI(h));sh.fill.solid();sh.fill.fore_color.rgb=PC.from_string(fill.lstrip('#'));sh.line.fill.background();return sh

def slide(num,title,sub=''):
 sl=P.slides.add_slide(P.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=PC.from_string('F4F7FB');t(sl,.65,.35,12,.25,'VEHICLE DAMAGE PROJECT | PROPOSAL DEFENCE',11,TEAL,True);t(sl,.65,1.02,12,.95,title,31,bold=True)
 if sub:t(sl,.69,2.03,12,.58,sub,17,MUTED)
 t(sl,.7,7.09,11,.22,'Working title • no trained-model test results claimed',10,MUTED);t(sl,12.1,7.02,.6,.3,str(num),15,TEAL,True);return sl
speech=[
('My project',25,'Good morning. My project uses photos to find visible damage on passenger cars and suggest the next step. It is a first visual check, not a full safety inspection. Today, I will explain the problem, the photos already checked, the workflow, and how I plan to test the system.'),
('Three answers',35,'The system gives three possible answers. Low visible concern means enough clear views show only small damage, or no visible damage. It does not mean the car is safe. Do not drive means a clear serious problem can be seen, such as a shredded tire. Inspection required means the photos are unclear or leave an important question. Every answer explains the visible reason and the next step. A photo cannot prove that the brakes or steering work.'),
('Our photo sources',40,'The earlier project audit reports thirteen thousand, nine hundred and forty-five VehiDE photos, with over thirty-six thousand marked damage areas. Those areas are not extra photos. We also have a small sample of thirty-six photos, but the expert reviews are not finished. CarDD is another possible source with four thousand photos, subject to permission. The goal is more than twenty thousand useful real photos. We must remove copies and check rights first. These photos do not yet have verified roadworthiness outcomes.'),
('Research workflow',45,'The research has five steps. First, check permission, count files, and remove copies. Second, ask reviewers to record visible damage and the suggested action. Third, keep photos of the same car together and separate the data for learning, choosing settings, and final testing. Fourth, compare a simple image model with a version that finds damaged areas and applies clear action rules. Several views can be combined only when they really belong to the same car. Finally, freeze the settings, run the final test and explain the mistakes.'),
('One car through the system',40,'For one car, the user adds photos. If none are usable, the system asks for clearer photos. Otherwise, the model finds visible damage. Clear serious danger leads to do not drive, even when other views are missing. If there is no clear hazard but the photos are incomplete or an important issue is unresolved, the answer is inspection required. Only enough clear evidence of small or no visible damage can support low visible concern. The system then explains the reason and the next step.'),
('How I will test it',45,'The most important mistake is when an expert says do not drive, but the model says low visible concern. I will count this mistake out of all expert do-not-drive cases. I will also report how well each of the three answers works and how many cases go to inspection. Sending every case to inspection is not enough to show useful performance. I will choose settings before the final test and report real mistakes, including poor lighting, missing views, glass, tires and possible leaks. Model tests have not been run yet.'),
('Next steps',25,'Next, I will finish the small review trial, check the data rights and groups, then train and compare the two models. After the final tests, I will write the seventy-page report and document the limits. The aim is clear advice from visible damage, not a replacement for a mechanic. Thank you.')]
sl=slide(1,'Vehicle Damage Assessment from Images','Using car photos to suggest the next step');bx(sl,.75,3.1,11.8,2.5,NAVY);t(sl,1.1,3.52,11,.65,'PHOTO  →  VISIBLE DAMAGE  →  NEXT STEP',29,'#FFFFFF',True);t(sl,1.1,4.53,11,.65,'Photos cannot prove that a car is safe to drive.',24,'#DDF3EF')
sl=slide(2,'Three answers, each with a reason','Different damage needs a different next step.')
for i,(a,b,col) in enumerate([('LOW VISIBLE CONCERN','Small surface damage; enough views.\nRoadworthiness was not verified.',MINT),('DO NOT DRIVE','Clear serious visible danger.\nAsk a professional before driving.',RED),('INSPECTION REQUIRED','Unclear views or unresolved concern.\nExplain what needs checking.',AMBER)]):
 y=2.91+i*1.05;bx(sl,.75,y,11.8,.91,col);t(sl,1,y+.2,3.9,.5,a,19,bold=True);t(sl,5.1,y+.12,7.0,.72,b,19)
sl=slide(3,'What we have—and what still needs work','Figures below come from the earlier project audit, not a new file count.')
for x,v,lab in [(.75,'13,945','VehiDE photos'),(4.88,'36,081','Marked damage areas'),(9,'36','Sample photos chosen')]:bx(sl,x,2.98,3.58,1.48,'#FFFFFF');t(sl,x+.2,3.12,3.2,.65,v,36,TEAL,True);t(sl,x+.2,3.91,3.2,.35,lab,18)
t(sl,.9,4.92,11.6,.75,'Goal: more than 20,000 useful real photos—not copies.',25,bold=True);t(sl,.9,5.87,11.5,.6,'Expert labels, final unique counts and linked safety outcomes are still open.',20,MUTED)
sl=slide(4,'Research workflow: five clear steps','The detailed diagram is in the printed proposal and backup slides.')
for i,(title,body) in enumerate([('1  CHECK DATA','Permission\nCopies and car groups'),('2  REVIEW','Small trial\nExpert action labels'),('3  SPLIT','Train\nValidation / test'),('4  COMPARE','Simple model\nDamage + rules'),('5  TEST','Freeze settings\nExplain mistakes')]):
 x=.7+i*2.52;bx(sl,x,3.05,2.33,2.05,MINT if i%2==0 else '#FFFFFF');t(sl,x+.17,3.3,2,.4,title,17,TEAL,True);t(sl,x+.17,4.04,2,.9,body,19)
t(sl,.85,5.73,11.7,.7,'Never train on one photo of a car and test on another photo of that same car.',22,bold=True)
sl=slide(5,'What happens when a user adds car photos?','Clear danger comes first. Missing information must not become a safety claim.')
for i,(a,b,col) in enumerate([('1  PHOTO CHECK','No usable photo? Ask for clearer views.',PALE),('2  DAMAGE CHECK','Clear serious hazard? Do not drive.',RED),('3  COVERAGE CHECK','Missing views or unresolved concern? Inspection.',AMBER),('4  LIMITED LOW CONCERN','Only small or no damage in enough clear views.',MINT)]):
 y=2.76+i*.84;bx(sl,.8,y,11.7,.7,col);t(sl,1,y+.17,3.5,.36,a,17,bold=True);t(sl,4.63,y+.15,7.5,.45,b,19)
sl=slide(6,'Avoid missing clear dangers—and measure useful answers','The reference is expert photo review, unless proper inspection records become available.')
bx(sl,.8,2.92,11.7,1.25,NAVY);t(sl,1.1,3.13,11.1,.46,'Main mistake: expert says “do not drive” → model says “low concern”',23,'#FFFFFF',True);t(sl,1.1,3.7,11,.3,'Count it out of all expert “do not drive” reference cases.',16,'#DDF3EF')
for i,a in enumerate(['Check all three answers, not just overall accuracy.','Count inspection requests. Sending every case is not enough.','Choose settings before the final test. Report real mistakes.']):t(sl,1,4.65+i*.6,11.5,.47,'• '+a,21)
sl=slide(7,'Next: review, build, test and write','A planned 70-page dissertation, with results that can be checked.')
for i,(a,b) in enumerate([('REVIEW','Finish the photo trial\nand permissions'),('BUILD','Train the first model\nand the improvement'),('TEST','Use separate cases\nand explain errors'),('WRITE','Record findings\nand the limits')]):
 x=.8+i*3.15;bx(sl,x,3,2.88,2.5,MINT if i%2==0 else '#FFFFFF');t(sl,x+.2,3.28,2.5,.4,a,19,TEAL,True);t(sl,x+.2,4.12,2.5,1,b,21)
t(sl,.9,6.06,11.6,.58,'Useful advice from photos—not proof of roadworthiness.',25,bold=True)
for i,(title,sec,words) in enumerate(speech):P.slides[i].notes_slide.notes_text_frame.text=f'{sec} seconds (target).\n\n{words}'
for nm in ['01_Research_Workflow','02_System_Workflow']:
 sl=slide(len(P.slides)+1,'Detailed workflow — questions only');img=Image.open(OUT/(nm+'.png'));w,h=img.size;hh=5.05;ww=hh*w/h;sl.shapes.add_picture(str(OUT/(nm+'.png')),PI((13.333-ww)/2),PI(1.87),width=PI(ww),height=PI(hh));sl.notes_slide.notes_text_frame.text='Backup only. Use the detailed version in the printed proposal for readable labels. Do not explain every box during the main talk.'
deck=OUT/'Presentation_Under_5_Minutes_v4.pptx'
with deck.open('xb') as f:P.save(f)

# Study guide contains the complete matched talk and targeted answers.
g=doc_setup('FOR REHEARSAL | NOT THE DOCUMENT TO HAND IN');g.add_heading('Understand your project before tomorrow',0)
g.add_paragraph('PRINT_Proposal.pdf is the document to print, based on your friend’s report. Check your teacher’s final instructions. This guide is for studying. Fill the identity blanks in the editable proposal before submission; the supplied PDF also contains blanks.')
g.add_heading('Your friend’s message, in simple English',1)
for text in ['Do not go over five minutes: they stop the presentation.','They mainly read the proposal, so it needs careful preparation.','Questions depend on the project.','The proposal is very important.','Print the proposal. The message does not say to print every support file.','Try to present early so you do not wait for hours. This is practical advice, not a verified university rule.']:g.add_paragraph(text,'List Bullet')
g.add_heading('One sentence to remember',1);g.add_paragraph('I am building a system that looks at car photos, explains the visible damage, and suggests the next step. It does not prove that the car is safe to drive.')
g.add_heading('What I prepared for you',1)
for text in ['An eight-page proposal: purpose, related work, questions, data, labeling, methods, two workflow figures, testing, schedule, risks and references.','Two detailed diagrams: how we will build and test the system; and how one car moves through the proposed decision process.','A seven-slide main talk with two question-only diagram backups. The speech targets 4 minutes 15 seconds, leaving 45 seconds before the five-minute stop. Actual timing needs rehearsal.','This simple guide explains the numbers, every main decision, and how to answer honestly when work is not finished.']:g.add_paragraph(text,'List Bullet')
g.add_heading('What has really been done?',1)
for text in ['Earlier work reports a VehiDE archive check: 13,945 files and 36,081 damage regions across 7 released label classes. I reviewed that record; I did not recount the archive for this proposal.','There is a 36-image DrBimmer sample. It is a sample, not 36 finished expert action labels.','The data-checking scripts and research documents exist in GitHub.','Model training, expert agreement, final test results and actual safety validation are NOT finished.']:g.add_paragraph(text,'List Bullet')
g.add_page_break();g.add_heading('Explain the research diagram in simple words',1)
for h,text in [
('1. Check the photos','Permission means we are allowed to use the photos for this study. We save where each photo came from. Remove copies so the count and test are not misleading.'),
('2. Ask people to review a small sample','Do not turn a label like scratch into a safety decision automatically. People record what they can see and the next action. A qualified car expert should help settle differences.'),
('3. Make three separate data groups','Training photos teach the model. Validation photos help choose settings. Test photos are the final exam. Photos of the same known car must stay in one group.'),
('4. Compare two versions','The first version is ResNet-18, a small existing image-model design with learned weights adapted to this task. The second finds damaged areas and applies clear rules. It can combine several views only if they are linked to the same car.'),
('5. Freeze and test','Stop changing the selected model and settings before final testing. Record what went wrong. If you change the model after seeing the test, that test is no longer a fresh final exam.')]:g.add_heading(h,2);g.add_paragraph(text)
g.add_heading('Explain the one-car diagram',1);g.add_paragraph('Follow the arrows: add photos → check if any are usable → find visible damage → ask if a serious hazard is clear. If yes, do not drive. If no, ask whether views are enough and concerns are resolved. Missing or unclear evidence means inspection. Only enough clear evidence of cosmetic or no visible damage can support low visible concern. Every branch explains the reason and next step.')
g.add_paragraph('Important: a shredded tire stays a do-not-drive case even if the rear view is missing. Do not use missing views to downgrade a clear hazard. A wet patch of unknown origin is not proof of brake-fluid leakage. A cropped scratch photo alone normally cannot support a whole-car low-concern answer.')
g.add_heading('Dataset numbers you must not mix up',1)
for text in ['13,945 = photo files reported in the earlier VehiDE audit. It is not a verified number of unique cars.','36,081 = marked damage areas inside those photos. One photo can have several areas.','36 = sample photos chosen for the small DrBimmer trial. Labels are still open.','2,300 = DrBimmer image rows in the earlier audit, not 2,300 confirmed safe cars.','4,000 = CarDD photos reported by the authors. Permission is required.','20,000+ = your new collection goal; 50,000+ is a stretch goal, not completed progress.','7 vs 8 = the earlier VehiDE file audit found 7 released classes, while the paper reports 8. Keep this difference visible.','79.8% = earlier overlap of minute-level filename groups across splits. It is NOT a measured rate of the same vehicles appearing in both groups.']:g.add_paragraph(text,'List Bullet')
questions=[
('What exactly is your project?','A first check from car photos. It explains the visible damage and suggests low visible concern, do not drive, or inspection required.'),
('Can you tell if a car is safe to drive?','Not fully. Photos cannot prove that brakes, steering or engine work. My current research target is expert-reviewed visual triage, not actual roadworthiness.'),
('What does triage mean?','It means a first decision about what should happen next. It is not a full inspection.'),
('Where do your photos come from?','The main source recorded so far is VehiDE. DrBimmer supplies an existing small trial sample. CarDD is another candidate, but needs permission. Other sources must pass rights and duplicate checks.'),
('How many cars do you have?','I cannot give a verified unique-car count yet. The earlier VehiDE audit reports 13,945 photo files. Several photos may show the same car.'),
('Why more than 20,000 photos?','It is a collection goal. I need different damage, lighting and viewpoints, not just a bigger number. Learning curves will show whether more data helps.'),
('What is an annotation or damage region?','It is a marked area in a photo, for example a box or outline around a dent. One photo may contain several regions.'),
('Who decides the correct answer?','The plan is independent reviewers with qualified automotive review. Their photo-based action labels are the reference unless proper linked inspection results become available. Those expert labels are not completed yet.'),
('Do your data have actual inspection results?','No adequate linked functional inspection outcomes have been verified yet. I must not turn a repair cost, damage name or salvage label into a safety verdict.'),
('Which models will you use?','ResNet-18 is the planned first image classifier. The improvement is a compact damage detector plus clear action rules and optional linked views. A YOLO-family detector is a candidate; the exact version and license must be chosen and recorded before implementation.'),
('Why ResNet-18?','It is a well-known, relatively small starting model. Starting from pretrained weights is practical for limited data and computing. Its suitability still needs testing on this project.'),
('What is transfer learning?','Start from a model that already learned general image features, then train it for this specific task instead of starting from nothing.'),
('What is new in your work?','The planned contribution is a careful comparison focused on visible evidence, false reassurance and inspection requests. I am not claiming I invented ResNet, YOLO or a new safety standard.'),
('What are training, validation and test?','Training teaches the model. Validation helps choose settings. Test is the separate final exam. I must not choose settings using the final test answers.'),
('Why group photos of the same car?','If the model learns one view of a car and is tested on another view of that car, the test may be easier than a genuinely new case.'),
('How do you find copies or the same car?','Use exact file or decoded-image hashes, then visual-similarity candidates and manual checks. Timestamps can suggest groups but cannot prove vehicle identity.'),
('How will you measure success?','The main error is an expert do-not-drive case predicted low visible concern. I count it out of all expert do-not-drive cases, and also report the other class results and inspection rate.'),
('Can you give a simple metric example?','Hypothetically, if 2 out of 40 expert do-not-drive cases were predicted low concern, that error would be 2/40 = 5%. This is only an explanation, not our result.'),
('Why not call every case inspection required?','That may avoid low-concern errors, but it gives little useful guidance. I will show the number sent for inspection together with missed serious cases and useful low-concern answers.'),
('What accuracy do you expect?','I will not promise a number before the pilot and experiments. Targets will be chosen after the pilot but before final testing.'),
('How do you handle glass?','Record where it is, how severe it is and whether it blocks the driver’s view. Broken glass alone is not enough to choose the action.'),
('What about a fluid leak?','A liquid patch may have many causes. If its source or safety meaning is unclear, the system should explain that and request inspection rather than naming a fluid from appearance.'),
('What if you have only one photo?','A clear serious hazard can still justify do not drive. A limited view often needs inspection. Multi-view comparison is done only when linked views actually exist.'),
('What is your current software status?','Research files, sample selection and data-audit scripts exist. The learned triage model has not been trained or tested. The diagrams describe the proposed design, not a working model.'),
('Is tomorrow’s presentation a live model demo?','This deck presents the proposal and planned workflow. I will not pretend to run a model that does not exist. If a live demo is required, I need to agree its scope with my supervisor.'),
('What if you cannot get enough expert reviewers?','I must report who supplied the labels and narrow the claim. I cannot call my own labels an independent expert reference.'),
('How do you protect data?','Follow licenses, hide personal information where permitted, and keep restricted photos and private inspection records out of the public repository. Save permitted code and summary results.'),
('Will you use ChatGPT or DeepSeek?','AI tools can help with coding, drafting and explanations. A trained image component must process the photos. AI-written text is not expert ground truth or proof of model performance; I must verify the work and follow university AI-disclosure rules.'),
('What if they ask about an unfinished detail?','Say: That choice is not finalized yet. My plan is to compare the options on validation data and record the result. Do not guess or claim an experiment was done.'),
('Why is the workflow detailed?','It shows the data checks, human review, separate test, and safety branches clearly. Each box has a real purpose. It is not complex just to stop questions.')]
g.add_page_break();g.add_heading('Likely questions and clear answers',1)
for q,a in questions:g.add_heading(q,2);g.add_paragraph(a)
g.add_page_break();g.add_heading('Short speaking script: aim for 4:15',1);g.add_paragraph('Seven main slides. Keep a 45-second buffer before the five-minute stop. Do not read the full detailed diagrams during the main talk. Rehearse twice; if your pace is slower, shorten examples rather than speak too fast.')
elapsed=0
for i,(title,sec,words) in enumerate(speech):elapsed+=sec;g.add_heading(f'Slide {i+1}: {title} | {sec} seconds | finish by {elapsed//60}:{elapsed%60:02}',2);g.add_paragraph(words)
g.add_heading('Tonight and tomorrow checklist',1)
for text in ['Fill your full name, student number, programme, supervisor, date and approved title in the Word proposal. If you have no final title, ask the teacher rather than silently treating the working title as approved.','Print the proposal. The PDF has 8 pages and identity blanks. Use the PDF for stable printing; if you change Word, check the new PDF before printing.','Open the PPTX on the actual presentation computer. Check font size and diagram clarity. Bring a local copy and a second copy on a USB drive.','Rehearse with a timer. Aim for 4:15, not exactly 5:00. Use the two detailed diagrams only when asked.','Read the questions about data counts, the model, test groups, expert labels and the main mistake. Explain them in your own words.','Do not say the model is finished, 20,000 images are collected, 79.8% is proven vehicle leakage, or a photo proves a car is safe.','Ask to present early if allowed. Arrive with the printed proposal and follow the teacher’s actual instructions.']:g.add_paragraph(text,'List Bullet')
guide=OUT/'READ_Defence_Guide_and_Script.docx'
with guide.open('xb') as f:g.save(f)
# Verification + preview renders from the actual printable PDF.
import pymupdf
pdf=pymupdf.open(proposal_pdf);assert len(pdf)==8,f'Proposal unexpectedly spans {len(pdf)} pages'
for i,pg in enumerate(pdf):
 assert pg.get_text().strip(),i
 assert pages[i]['title'] in pg.get_text(),(i,pg.get_text()[:100])
 pg.get_pixmap(matrix=pymupdf.Matrix(1,1)).save(OUT/f'preview_proposal_{i+1}.png')
assert len(Presentation(deck).slides)==9
assert len(Document(proposal_doc).inline_shapes)==2
assert sum(s[1] for s in speech)==255
for sl in Presentation(deck).slides:
 for sh in sl.shapes:assert sh.left>=0 and sh.top>=0 and sh.left+sh.width<=P.slide_width+10000 and sh.top+sh.height<=P.slide_height+10000
status={'proposal_pdf_pages':len(pdf),'main_slides':7,'backup_slides':2,'script_seconds':255,'script_words':sum(len(s[2].split()) for s in speech),'reference_count':len(refs),'expert_labels':'not completed','model_results':'not run','prior_data_audit':'reviewed, not reproduced'}
(OUT/'verification.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
print(json.dumps(status,indent=2));print('Deliverables:',proposal_pdf,proposal_doc,wf,deck,guide,sep='\n')
