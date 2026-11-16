from pathlib import Path
import ast, math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from docx import Document
from docx.shared import Inches as DIn, Pt as DPt, RGBColor as DC
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path.cwd(); OUT=ROOT/'presentation-redesign'; OUT.mkdir(exist_ok=True)
# Read prior talk content without running the prior file-generation script.
source = Path(__file__).with_name('build_proposal_pack.py')
if not source.exists():
 source = ROOT/'build_defence_pack.py'
tree=ast.parse(source.read_text(encoding='utf-8'))
slides=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='slides' for t in n.targets))
P=Presentation();P.slide_width=Inches(13.333);P.slide_height=Inches(7.5)
C={'navy':'112139','ink':'152B45','muted':'5B6D82','paper':'F4F7FB','white':'FFFFFF','teal':'087E83','mint':'DDF3EF','amber':'C17A0C','cream':'FFF0D5','red':'BA414B','rose':'FBE7E8','line':'DCE4EE','blue':'DDEAF9'}
def rgb(v):return RGBColor.from_string(C.get(v,v))
def box(s,x,y,w,h,fill='white',line=None,r=0):
 sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if r else MSO_SHAPE.RECTANGLE, Inches(x),Inches(y),Inches(w),Inches(h));sh.fill.solid();sh.fill.fore_color.rgb=rgb(fill)
 if line:sh.line.color.rgb=rgb(line)
 else:sh.line.fill.background()
 if r:
  try:sh.adjustments[0]=.12
  except:pass
 return sh
def txt(s,x,y,w,h,text,size=22,color='ink',bold=False,font='Aptos',align=None):
 sh=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=sh.text_frame;tf.word_wrap=True
 tf.margin_left=0;tf.margin_right=0;tf.margin_top=0;tf.margin_bottom=0
 for i,line in enumerate(text.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.space_after=Pt(6);p.font.name=font;p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=rgb(color);p.text=line
  if align is not None:p.alignment=align
 return sh
def line(s,x,y,w,h,color='line',width=1.5):
 sh=s.shapes.add_connector(1,Inches(x),Inches(y),Inches(x+w),Inches(y+h));sh.line.color.rgb=rgb(color);sh.line.width=Pt(width);return sh
def circle(s,x,y,d,fill,linecolor=None):
 sh=s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x),Inches(y),Inches(d),Inches(d));sh.fill.solid();sh.fill.fore_color.rgb=rgb(fill)
 if linecolor:sh.line.color.rgb=rgb(linecolor)
 else:sh.line.fill.background()
 return sh
def badge(s,x,y,w,label,fill='mint',color='teal'):
 box(s,x,y,w,.36,fill,r=1);txt(s,x+.12,y+.065,w-.2,.25,label,11,color,True)
def base(n,kicker,title,sub=None,dark=False):
 s=P.slides.add_slide(P.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=rgb('navy' if dark else 'paper')
 box(s,.52,.38,.1,.28,'teal' if not dark else '49D5C6');txt(s,.8,.4,11,.25,kicker.upper(),11,'muted' if not dark else 'AFC8DE',True)
 txt(s,.65,1.02,12.1,.95,title,34,'white' if dark else 'ink',True)
 if sub:txt(s,.68,1.95,12,.6,sub,17,'muted' if not dark else 'AFC8DE')
 line(s,.65,7.01,12.05,0,'line' if not dark else '38506A',.7)
 txt(s,.68,7.12,11.5,.2,'VEHICLE DAMAGE TRIAGE  /  PROPOSAL DEFENCE  /  WORKING TITLE',9,'muted' if not dark else 'AFC8DE')
 txt(s,12.15,7.08,.5,.27,f'{n:02}',13,'teal' if not dark else '49D5C6',True)
 return s

def car(s,x,y,scale=1,color='ink',hazard=True):
 # Original vector side silhouette: illustrative diagram, never a model result.
 pts=[(0,.9),(.25,.55),(1.25,.45),(1.95,0),(3.5,0),(4.25,.47),(5.3,.65),(5.6,.95),(5.6,1.45),(0,1.45)]
 # Freeform uses EMU-coordinate scaling for predictable sizing.
 b=s.shapes.build_freeform(Inches(x), Inches(y+.9*scale),scale=1)
 b.add_line_segments([(Inches(x+a*scale),Inches(y+c*scale)) for a,c in pts[1:]],close=True)
 body=b.convert_to_shape();body.fill.solid();body.fill.fore_color.rgb=rgb(color);body.line.fill.background()
 # Window panels, roofline and wheels.
 box(s,x+2.0*scale,y+.15*scale,.62*scale,.36*scale,'blue',r=1)
 box(s,x+2.75*scale,y+.15*scale,.68*scale,.36*scale,'blue',r=1)
 for wx in (.88,4.35):
  circle(s,x+(wx-.4)*scale,y+1.03*scale,.8*scale,'navy');circle(s,x+(wx-.23)*scale,y+1.2*scale,.46*scale,'muted');circle(s,x+(wx-.08)*scale,y+1.35*scale,.16*scale,'paper')
 if hazard:
  line(s,x+4.04*scale,y+.73*scale,.55*scale,.21*scale,'red',3)
  line(s,x+4.14*scale,y+.85*scale,.52*scale,.19*scale,'red',3)
 return body

# 1 — title / hero
s=base(1,'BSc dissertation • research proposal','',dark=True)
txt(s,.7,1.25,7.2,1.85,'Vehicle Damage\nAssessment from Images',37,'white',True)
txt(s,.73,3.17,6.5,.65,'Evidence-based driveability triage',23,'49D5C6')
txt(s,.74,4.16,6.1,1.05,'Recognize visible damage.\nExplain the next step. Know the limits.',22,'white')
badge(s,.74,5.72,3.65,'FIVE-MINUTE PROPOSAL DEFENCE','263E57','white')
# Vertical information panel
box(s,8.15,1.25,4.5,5.22,'1B344F',r=1)
car(s,8.5,2.15,.68,'DDEAF9')
txt(s,8.55,4.03,3.7,.32,'PHOTO → EVIDENCE → ACTION',14,'49D5C6',True)
txt(s,8.55,4.62,3.5,.9,'Not a roadworthiness\ncertificate.',22,'white',True)
txt(s,.75,6.42,7,.23,'Working title • presenter / supervisor details to confirm',11,'AFC8DE')

# 2 — visual problem
s=base(2,'01 / Motivation','The same word “damage” hides very different risks.','A useful system must distinguish visible evidence from what a photograph cannot tell us.')
items=[('01','COSMETIC','Shallow body-panel scratch','Describe the visible finding.','mint','teal'),('02','VISIBLE HAZARD','Shredded tire or displaced wheel','Recommend professional assessment before driving.','rose','red'),('03','UNRESOLVED','Missing angle or possible leak','Explain what needs inspection.','cream','amber')]
for i,(num,label,ex,action,fill,col) in enumerate(items):
 x=.7+i*4.08;box(s,x,2.88,3.86,2.82,'white',r=1);circle(s,x+.24,3.12,.52,fill);txt(s,x+.36,3.24,.4,.22,num,12,col,True)
 txt(s,x+.24,3.91,3.38,.32,label,15,col,True);txt(s,x+.24,4.4,3.38,.6,ex,22,'ink',True);txt(s,x+.24,5.09,3.35,.5,action,14,'muted')
box(s,.7,6.05,12.02,.57,'navy',r=1);txt(s,.95,6.21,11.5,.27,'Appearance alone cannot verify the brakes, steering or engine.',18,'white',True)

# 3 — categories
s=base(3,'02 / Decision framework','Three outputs. Every one needs a reason.','The action is bounded by the submitted views—not a claim about hidden mechanical function.')
for i,(label,col,fill,reason,action) in enumerate([
('LOW VISIBLE CONCERN','teal','mint','Minor cosmetic findings; sufficient visual coverage.','“Roadworthiness was not verified.”'),
('DO NOT DRIVE','red','rose','Clear serious visible hazard, such as a shredded tire.','Professional assessment before driving.'),
('INSPECTION REQUIRED','amber','cream','Unclear views or unresolved safety-critical concern.','State what needs a closer or hands-on check.')]):
 y=2.87+i*1.03;box(s,.72,y,11.9,.88,'white',r=1);box(s,.72,y,.08,.88,col);txt(s,.97,y+.17,3.3,.52,label,16,col,True);txt(s,4.17,y+.13,4.3,.65,reason,17);txt(s,8.87,y+.16,3.48,.61,action,16,'muted')
badge(s,.75,6.3,11.85,'GLASS: location + extent + driver visibility • “broken glass” alone is not an action label.','blue','ink')

# 4 — data dashboard
s=base(4,'03 / Data and completed preparation','A real starting point—not a finished dataset.','Existing repository audit reviewed at commit 3482f30; raw-data counts were not repeated in this session.')
for x,num,label in [(.75,'13,945','VehiDE image files'),(4.85,'36,081','Annotated damage regions'),(8.95,'36','Pilot images sampled')]:
 box(s,x,2.83,3.65,1.52,'white',r=1);txt(s,x+.23,3.02,3.25,.65,num,38,'teal',True);txt(s,x+.23,3.77,3.25,.32,label,17,'muted')
box(s,.75,4.65,7.63,1.6,'navy',r=1);txt(s,1,4.87,7.1,.3,'COLLECTION GOAL',12,'49D5C6',True);txt(s,1,5.29,6.95,.56,'20,000+ usable real images',28,'white',True);txt(s,1,5.94,6.95,.24,'50,000+ stretch goal • not an achieved total',12,'AFC8DE')
box(s,8.65,4.65,3.95,1.6,'cream',r=1);txt(s,8.9,4.89,3.4,.42,'Expert labels still open',19,'amber',True);txt(s,8.9,5.47,3.4,.62,'Inspection-backed outcomes\nnot verified.',17,'ink')
txt(s,.8,6.48,11.8,.27,'More sources ≠ more unique vehicles. Rights, duplicates and incident grouping must be checked.',13,'muted')

# 5 — method pipeline
s=base(5,'04 / Proposed method','Build a baseline. Then test a practical improvement.','A reproducible comparison—not an assumption that a more complex model will be better.')
for i,(lab,desc,fill,col) in enumerate([
('PHOTO INPUT','Image-capable model\nQuality and view checks','blue','ink'),
('VISIBLE EVIDENCE','Damage localization\nMulti-view pooling if linked','mint','teal'),
('ACTION POLICY','Category + reason\nNext step + limitation','navy','white')]):
 x=.8+i*4.1;box(s,x,2.95,3.55,1.72,fill,r=1);txt(s,x+.22,3.17,3.1,.3,lab,14,col,True);txt(s,x+.22,3.69,3.1,.75,desc,20,col)
 if i<2:txt(s,x+3.67,3.49,.45,.6,'→',28,'teal',True)
box(s,.82,5.13,11.7,.97,'white',r=1);txt(s,1.05,5.31,2.6,.3,'BASELINE',12,'muted',True);txt(s,3.6,5.28,8.55,.62,'Transfer-learning image classifier → compare on the same frozen test cases',20,'ink')
txt(s,.85,6.42,11.5,.25,'Current repository: data-audit scaffold. Proposed model training and inference are not yet implemented.',13,'muted')

# 6 — labeling/splits
s=base(6,'05 / Labeling and independence','Get the reference labels right before scaling.','Keep observation, recommended action and verified inspection outcome as separate records.')
box(s,.75,2.83,5.85,3.61,'white',r=1);txt(s,1.02,3.08,5.3,.43,'Pilot → disagreement review → scale',23,'ink',True)
for j,(a,b) in enumerate([('START','36 existing samples; extend toward 60 cases'),('REVIEW','Two independent reviewers + qualified adjudication'),('STRESS TEST','Glass, tires/wheels, missing views, possible leakage')]):
 yy=3.83+j*.76;txt(s,1.04,yy,1.2,.28,a,11,'teal',True);txt(s,2.5,yy-.02,3.75,.6,b,17,'ink')
box(s,6.87,2.83,5.7,3.61,'navy',r=1);txt(s,7.16,3.08,5.05,.43,'Keep related photos together',23,'white',True)
for j,label in enumerate(['Deduplicate across sources before splitting.','Group known vehicles / incidents in one split.','Timestamp groups are proxies—not vehicle IDs.']):
 yy=3.84+j*.76;circle(s,7.17,yy+.03,.13,'49D5C6');txt(s,7.48,yy,4.67,.6,label,18,'white')

# 7 — metric / illustrative diagram
s=base(7,'06 / Evaluation','Reduce false reassurance—without deferring everything.','Thresholds selected on validation data. Numerical targets locked before final testing.')
box(s,.75,2.8,7.45,1.73,'navy',r=1);txt(s,1,3.04,6.9,.28,'PRIMARY VISUAL-TRIAGE ERROR',12,'49D5C6',True)
txt(s,1,3.53,6.85,.36,'Expert “do not drive” → predicted “low concern”',21,'white',True)
line(s,1,4.02,6.75,0,'AFC8DE',1);txt(s,1.05,4.12,6.65,.27,'Divided by all expert “do not drive” reference cases',15,'AFC8DE')
for j,t in enumerate(['Error counts + uncertainty','Per-class precision / recall + confusion matrix','Inspection-referral rate + useful low-concern coverage']):
 txt(s,.96,4.96+j*.45,7.0,.36,'• '+t,17,'ink')
box(s,8.52,2.8,4.04,3.78,'white',r=1);txt(s,8.8,3.05,3.48,.58,'Evaluate the trade-off',22,'ink',True)
# Conceptual balance graphic rather than an invented results plot.
line(s,9.0,4.62,3.0,0,'ink',2);line(s,10.5,4.62,0,1,'ink',2);circle(s,10.38,4.49,.24,'teal')
box(s,8.94,4.1,1.28,.42,'rose',r=1);txt(s,9.03,4.2,1.15,.22,'MISSES',11,'red',True)
box(s,10.81,4.1,1.3,.42,'cream',r=1);txt(s,10.9,4.2,1.17,.22,'REFERRALS',11,'amber',True)
txt(s,8.84,5.87,3.36,.44,'All-inspection ≠ useful success',15,'muted',True)

# 8 — roadmap / closing
s=base(8,'07 / Roadmap and contribution','From a proposal to a defensible 70-page study.','Relative milestones; calendar dates depend on the confirmed university deadline.',dark=True)
for i,(num,title,desc) in enumerate([('1','CONFIRM','Title, language, deadline\nand handbook'),('2','CURATE','Rights, deduplication\nand expert pilot'),('3','COMPARE','Baseline + improvement\nand frozen evaluation'),('4','DOCUMENT','Results, failure cases\nand reproducible report')]):
 x=.79+i*3.12;circle(s,x,3.0,.57,'49D5C6');txt(s,x+.18,3.13,.29,.3,num,19,'navy',True)
 if i<3:line(s,x+.73,3.28,2.15,0,'38506A',2)
 txt(s,x,3.98,2.8,.34,title,16,'49D5C6',True);txt(s,x,4.52,2.8,.8,desc,20,'white')
box(s,.79,5.79,11.8,.75,'263E57',r=1);txt(s,1.04,5.98,11.2,.4,'The contribution: explainable visual triage—not proof that a car is safe to drive.',22,'white',True)

# Existing speaker content matches conceptual core; swap slide 5/6 as new layout orders them.
order=[0,1,2,3,5,4,6,7]
for idx,old in enumerate(order):
 sec=slides[old][3];speech=slides[old][4]
 P.slides[idx].notes_slide.notes_text_frame.text=f'SLIDE {idx+1} | target {sec} seconds\n\n{speech}\n\nPROPOSAL STAGE: no trained-model performance results are claimed.'
# Backup sources: only compact citations and claim provenance, not reading slides.
for n,(title,entries) in enumerate([
('Evidence for the current starting point',[
('R1 · Repository audit at 3482f30','docs/07_vehide_audit.md','13,945 files; 36,081 regions; 7 released classes. Prior audit, not re-run here.'),
('R2 · Existing pilot','pilot/04_pilot_report.md','36 samples; expert labels and agreement open.'),
('Caution · Incident grouping','docs/08_continuation_review.md','79.8% is timestamp-group overlap, not confirmed vehicle leakage.')]),
('Dataset candidates: access is not guaranteed',[
('CarDD · 4,000 images','https://cardd-ustc.github.io/','Original permission form required; redistribution restricted.'),
('VehiDE · original research / distribution','https://cvis.hcmute.edu.vn/Research/Details/4','Publication reports 8 classes; prior archive audit found 7.'),
('Roboflow · 19,100 listed in v1','universe.roboflow.com/tarpit-patel-uyibg/car_damages_19k/dataset/1','Indexed count only; rights, provenance and overlap pending.')])],start=9):
 s=base(n,'Backup / not part of timed talk',title)
 for j,(h,url,desc) in enumerate(entries):
  y=2.85+j*1.14;txt(s,.86,y,11.7,.38,h,21,'teal',True);txt(s,.86,y+.43,11.7,.33,desc,17,'ink');txt(s,.86,y+.81,11.7,.22,url,11,'muted')
 s.notes_slide.notes_text_frame.text='Backup only. Sources were reviewed during the earlier research session. See research source ledger and continuation review for complete limitations. Do not add source counts into a unique-image total.'

ppt=OUT/'Vehicle_Damage_Proposal_Designed_v2.pptx'
with ppt.open('xb') as f:P.save(f)

# Polished Word rehearsal script, one timed-slide section per page (cover + 8 pages).
D=Document();sec=D.sections[0];sec.top_margin=DIn(.7);sec.bottom_margin=DIn(.65);sec.left_margin=DIn(.85);sec.right_margin=DIn(.85)
D.styles['Normal'].font.name='Calibri';D.styles['Normal'].font.size=DPt(12);D.styles['Normal'].paragraph_format.space_after=DPt(10)
D.styles['Normal'].paragraph_format.line_spacing=1.15
for nm in ['Title','Heading 1','Heading 2']:
 D.styles[nm].font.name='Calibri';D.styles[nm].font.color.rgb=DC.from_string(C['ink'])
D.styles['Title'].font.size=DPt(31)
D.styles['Heading 1'].font.size=DPt(24)
header=sec.header.paragraphs[0];header.text='VEHICLE DAMAGE TRIAGE  |  PROPOSAL DEFENCE';header.style='Caption'
foot=sec.footer.paragraphs[0];foot.text='Rehearsal script • working title • '
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');foot._p.append(fld)
D.add_paragraph('FIVE-MINUTE\nDEFENCE SCRIPT','Title')
D.add_paragraph('Vehicle Damage Assessment from Images\nfor Driveability Triage','Subtitle')
D.add_paragraph('Matches: Vehicle_Damage_Proposal_Designed_v2.pptx')
D.add_heading('How to use this script',1)
for t in ['Read only the “Say” paragraphs during rehearsal. Stage directions and reminders are not part of the spoken talk.','Eight core slides total 300 seconds. The two source slides are for questions only. Approximately 640 spoken words; rehearse with a timer and use natural pauses.','English and the title remain provisional until confirmed. Presenter and supervisor details have intentionally not been invented.','This is a proposal defence—not a live demonstration or a presentation of completed model results.']:
 D.add_paragraph(t,style='List Bullet')
D.add_heading('Timing at a glance',2)
table=D.add_table(rows=1, cols=3);table.style='Light Shading Accent 1'
for c,t in zip(table.rows[0].cells,['Slide','Seconds','Cumulative']):c.text=t
elapsed=0
names=['Title and aim','The problem','Three outputs','Data and current progress','Proposed method','Pilot and independence','Evaluation','Roadmap and contribution']
cues=['State the aim calmly. Do not call the vehicle safe.','Point to the three different risk situations.','Read the category names clearly; explain the limited scope.','Separate prior audit counts from the future collection goal.','Follow the pipeline left to right; mention the baseline comparison.','State that expert labels are still open; timestamps are not vehicle IDs.','Name the numerator and denominator; stress the referral trade-off.','Finish with the contribution, not a claim of completed results.']
for i,k in enumerate(order):
 secs=slides[k][3];elapsed+=secs;cells=table.add_row().cells
 for c,t in zip(cells,[f'{i+1}. {names[i]}',str(secs),f'{elapsed//60}:{elapsed%60:02}']):c.text=t
for i,k in enumerate(order):
 D.add_page_break();D.add_paragraph(f'SLIDE {i+1:02}  /  {slides[k][3]} SECONDS','Subtitle');D.add_heading(names[i],1)
 D.add_paragraph('Stage direction: '+cues[i],style='Caption');D.add_heading('Say',2)
 D.add_paragraph(slides[k][4]);D.add_heading('Remember',2)
 reminders=[
 'Use the approved title if it differs from the working title. Introduce your name verbally once confirmed.',
 'A photograph cannot establish that brakes, steering or engine work correctly.',
 'Glass location, severity and driver visibility matter. A generic label does not determine an action.',
 'Counts are from the prior repository audit, not re-audited here. The target is >20,000 usable real unique images; 50,000+ is conditional. No final deduplicated vehicle total is established.',
 'Current tracked work contains research and data-audit scripts, not a trained triage inference model.',
 'The 36-image sample is real preparation. The 60-case extension and two-reviewer expert evaluation remain planned.',
 'No numerical model performance results exist. An all-inspection policy must not be presented as useful success.',
 'Ask whether a live software demo is also required. The screenshot explicitly asks for a five-minute presentation, not a proven functioning model.'
 ]
 D.add_paragraph(reminders[i])
D.add_page_break();D.add_heading('Short answers for questions',1)
qa=[('Can this system say a car is safe to drive?','No. It recommends a preliminary action from visible evidence. Roadworthiness requires adequate hands-on and functional checks.'),('How many images are available?','The prior VehiDE archive audit reports 13,945 files and 36,081 damage regions. A 36-image pilot sample exists with labels open. Final cross-source unique totals remain unverified.'),('What does the 79.8% overlap mean?','Parsed validation filenames share minute-level timestamp groups with training. This is a candidate leakage warning, not verified same-vehicle overlap.'),('Why 20,000 or 50,000 images?','Those are collection goals, not guaranteed requirements for model quality. Learning curves, rights, diversity and hazard coverage will guide expansion.'),('Where are the model results?','Model training and held-out evaluation have not been run. This proposal explains how they will be carried out.'),('What if every case requires inspection?','We will report referral rate and useful low-concern coverage as well as missed serious cases; all-inspection is a comparator, not an automatic success.')]
for q,a in qa:D.add_heading(q,2);D.add_paragraph(a)
D.add_heading('Submission requirement clarification',1)
D.add_paragraph('The teacher screenshot explicitly requests a five-minute presentation. It also says that the two supplied Chinese Word documents are examples of files to prepare: a graduation project task sheet (任务书) and an opening/proposal report (开题报告). This suggests written proposal-stage documents may also be expected, but the screenshot alone does not establish exactly which must be submitted, when, or whether both must be authored by the student. Confirm those points with the teacher. The earlier dataset inventory, pilot extension and evaluation plan were research-support deliverables from the broader project request—not requirements proven by the Chinese examples. This speaking script is a rehearsal aid, not a confirmed teacher-required submission.')
word=OUT/'Five_Minute_Defence_Script_v2.docx'
with word.open('xb') as f:D.save(f)
# Structural checks; no claim of GUI rendering or exact Word pagination.
Q=Presentation(ppt);assert len(Q.slides)==10
assert len(Document(word).paragraphs)>50
assert sum(slides[k][3] for k in order)==300
for ii,sl in enumerate(Q.slides):
 for sh in sl.shapes:
  assert sh.left>=0 and sh.top>=0 and sh.left+sh.width <= Q.slide_width+15000 and sh.top+sh.height <= Q.slide_height+15000,(ii,sh.name)
print('Verified:',ppt,word,sep='\n');print('Core slides: 8; backup: 2; target: 300 seconds; original vector artwork, no invented result graphics.')
