from pathlib import Path
import json,hashlib,shutil
from PIL import Image, ImageOps,ImageDraw,ImageFont
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from docx import Document
ROOT=Path.cwd(); OUT=ROOT/'photo-presentation-v5-final';OUT.mkdir(exist_ok=True);AS=OUT/'images';AS.mkdir(exist_ok=True)
assets=[
('m4_roof_down.jpg','2022 BMW M4 Competition Convertible.jpg','Calreyn88','CC BY-SA 4.0','https://creativecommons.org/licenses/by-sa/4.0/','https://commons.wikimedia.org/wiki/File:2022_BMW_M4_Competition_Convertible.jpg'),
('suv_roof_crush.jpg','CR-V-Accident.jpg','Ryanandlenny','CC BY 3.0','https://creativecommons.org/licenses/by/3.0/','https://commons.wikimedia.org/wiki/File:CR-V-Accident.jpg'),
('flat_tire.jpg','Broken tire.jpg','Tiia Monto','CC BY-SA 4.0','https://creativecommons.org/licenses/by-sa/4.0/','https://commons.wikimedia.org/wiki/File:Broken_tire.jpg'),
('front_damage.jpg','cosmetic-scratches-pexels.jpg','Uiliam Nörnberg','Pexels License','https://www.pexels.com/license/','https://www.pexels.com/photo/close-up-of-the-side-of-a-car-with-scratches-on-the-front-fender-24960483/')]
records=[]
for dest,src,author,lic,licurl,page in assets:
 source=ROOT/'photo-assets'/src
 if not source.exists():source=ROOT/'presentations/real-photo-v5/images'/dest
 im=Image.open(source);im=ImageOps.exif_transpose(im).convert('RGB');im.thumbnail((2000,1600));im.save(AS/dest,quality=93)
 records.append(dict(file=dest,author=author,license=lic,license_url=licurl,source=page,changes='Resized and JPEG re-encoded; aspect ratio retained. Any detail crop explicitly labeled.',role='Presentation illustration only; not a dataset acquisition or expert test label.',sha256=hashlib.sha256((AS/dest).read_bytes()).hexdigest()))
# Detail deliberately excludes unrelated areas; never use this crop to label the whole vehicle low concern.
source=ROOT/'photo-assets/cosmetic-scratches-pexels.jpg'
if not source.exists():source=ROOT/'presentations/real-photo-v5/images/front_damage.jpg'
im=Image.open(source);w,h=im.size;im.crop((int(.02*w),int(.50*h),int(.64*w),int(.68*h))).save(AS/'surface_detail.jpg',quality=93)
records.append(dict(file='surface_detail.jpg',author='Uiliam Nörnberg',license='Pexels License',license_url='https://www.pexels.com/license/',source=assets[3][5],changes='Detail crop of lower front bumper scrapes; remainder of damaged vehicle deliberately not shown. Derived from front_damage.jpg source, not a separate example.',role='Visible surface-finding illustration only; insufficient whole-car coverage.'))
base=ROOT/'tomorrow-defence-ready/Presentation_Under_5_Minutes_v4.pptx'
if not base.exists():base=ROOT/'presentations/tomorrow-defence/Presentation_Under_5_Minutes_v4.pptx'
P=Presentation(base)
NAVY='152B45';TEAL='087E83';MUTED='516479'
def tx(sl,x,y,w,h,text,size=22,col=NAVY,bold=False):
 sh=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=sh.text_frame;tf.word_wrap=True;tf.margin_left=0;tf.margin_right=0;tf.margin_top=0;tf.margin_bottom=0
 for i,ln in enumerate(text.split('\n')):
  p=tf.paragraphs[0] if not i else tf.add_paragraph();p.text=ln;p.font.name='Arial';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(col)
 return sh
def box(sl,x,y,w,h,fill):
 sh=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h));sh.fill.solid();sh.fill.fore_color.rgb=RGBColor.from_string(fill);sh.line.fill.background()
def new(title,sub):
 sl=P.slides.add_slide(P.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=RGBColor.from_string('F4F7FB');tx(sl,.65,.3,12,.3,'REAL PHOTOS | PROPOSED RESEARCH, NOT MODEL RESULTS',11,TEAL,True);tx(sl,.65,.87,12,1,title,30,bold=True);tx(sl,.68,1.9,12,.6,sub,17,MUTED);return sl

def contain(sl,path,x,y,w,h):
 im=Image.open(path);iw,ih=im.size;r=min(w/iw,h/ih);ww=iw*r;hh=ih*r;sl.shapes.add_picture(str(path),Inches(x+(w-ww)/2),Inches(y+(h-hh)/2),width=Inches(ww),height=Inches(hh))
def move_last(index):
 ids=P.slides._sldIdLst;item=ids[-1];ids.remove(item);ids.insert(index,item)

sl=new('Damage does not always mean the same next step','Real photo examples • explanations, not confirmed roadworthiness labels')
cols=[('surface_detail.jpg','SURFACE MARKS','A cosmetic-looking detail.\nThis crop alone needs more views.','U. Nörnberg / Pexels • detail crop','DDF3EF'),('flat_tire.jpg','CLEAR VISIBLE HAZARD','Tire visibly flat on the ground.\nDo not drive before assistance.','Tiia Monto • CC BY-SA 4.0','FBE7E8'),('front_damage.jpg','INSPECTION REQUIRED','Scrapes and damaged front area.\nHidden effects cannot be checked.','U. Nörnberg / Pexels • full photo','FFF0D5')]
for i,(fn,title,cap,credit,col) in enumerate(cols):
 x=.65+i*4.23;box(sl,x,2.65,4.03,3.02,'FFFFFF');contain(sl,AS/fn,x+.08,2.71,3.87,2.9);box(sl,x,5.86,4.03,.41,col);tx(sl,x+.12,5.95,3.8,.3,title,15,bold=True);tx(sl,x+.08,6.39,3.9,.59,cap,15);tx(sl,x+.08,7.12,3.9,.19,credit,9,MUTED)
sl.notes_slide.notes_text_frame.text='Target: 20 seconds. These examples show why damage alone is not the final answer. Surface marks may be cosmetic, but a cropped photo still needs more views. A visibly flat tire is a clear reason not to drive before assistance. The damaged front area needs inspection. These are licensed illustration photos, not verified inspection labels. Left and right panels derive from the same source photo.'
move_last(1)
sl=new('Open by design—or crushed by an accident?','The model must learn the difference, not just look for a missing roof.')
for x,fn,title,col,cap,credit in [(.65,'m4_roof_down.jpg','BMW M4 CONVERTIBLE • ROOF DOWN','DDF3EF','Factory roof-down design is not roof damage.','Calreyn88 • CC BY-SA 4.0'),(6.85,'suv_roof_crush.jpg','HONDA CR-V • ROOF CRUSH','FBE7E8','Visible roof deformation + damaged windshield.','Ryanandlenny • CC BY 3.0')]:
 box(sl,x,2.65,5.83,3.17,'FFFFFF');contain(sl,AS/fn,x+.05,2.7,5.73,3.07);box(sl,x,5.95,5.83,.44,col);tx(sl,x+.12,6.05,5.55,.28,title,16,bold=True);tx(sl,x+.05,6.51,5.73,.43,cap,18);tx(sl,x+.05,7.14,5.73,.18,credit+' • resized; full sources in credits',9,MUTED)
sl.notes_slide.notes_text_frame.text='Target: 25 seconds. This BMW is designed to open its roof. Roof down does not mean damage. The SUV has a visibly crushed roof and damaged windshield. My planned model should learn real deformation, not label every open roof as an accident. I will test roof-up and roof-down convertibles, ordinary cars and real roof-damage cases. A convertible can still have other damage. This comparison is a research plan, not a tested result.'
move_last(2)
# One concise backup to defend the proposed distinguishing point.
sl=new('How I will test this difficult example','Planned design-aware challenge set • not a new model result')
for y,h,b in [(2.85,'INCLUDE NORMAL DESIGN','Convertibles with roof up and roof down, from different models and settings.'),(3.95,'INCLUDE REAL DAMAGE','Damaged fixed roofs AND damaged convertibles. Do not learn “SUV = damage”.'),(5.05,'TEST ON NEW CARS','Keep each car in one split. Review false roof-damage alarms and missed roof damage.')]:
 box(sl,.8,y,11.7,.88,'FFFFFF');tx(sl,1,y+.18,3.1,.5,h,17,TEAL,True);tx(sl,4.2,y+.12,7.95,.62,b,19)
tx(sl,.85,6.34,11.7,.65,'Roof design alone never decides the whole-car category. Missing or unclear evidence still needs inspection.',20,bold=True)
sl.notes_slide.notes_text_frame.text='Question-only backup. This is a proposed stress test, not established novelty or demonstrated accuracy. Record roof design, roof state, real deformation and uncertainty separately. Test unseen vehicle groups and report denominators. Training and challenge examples must not overlap. Control source/background shortcuts; include damaged convertibles as well as undamaged SUVs.'
# Credits slides sufficient attribution for each image, including direct license links.
for start in [0,2]:
 sl=new('Photo credits and use conditions','Backup only • real illustrations, not photographs from the audited training collection')
 for j,rec in enumerate(records[start:start+2]):
  y=2.75+j*1.75;tx(sl,.85,y,11.7,.4,rec['file']+' — '+rec['author'],21,TEAL,True);tx(sl,.85,y+.5,11.7,.8,rec['source']+'\n'+rec['license']+' • '+rec['license_url'],14);tx(sl,.85,y+1.28,11.6,.3,'Resized for layout; no claim of photographer or brand endorsement.',12,MUTED)
 tx(sl,.85,6.54,11.6,.44,'Surface-detail crop: same Pexels photograph as front_damage.jpg; not a separate car.',15,MUTED)
 sl.notes_slide.notes_text_frame.text='Photo licenses apply to their respective images. BMW and flat-tire photo derivatives remain CC BY-SA 4.0. CR-V photo is CC BY 3.0. Pexels use follows the Pexels License; do not assume machine-learning rights from a presentation use. Full attributions and modifications are recorded in PHOTO_SOURCES.md.'
# Replace main speech to budget the extra visual slides; preserve all slide layouts and runs.
main=[
(20,'Good morning. My project uses photos to explain visible car damage and suggest the next step. It is a first visual check, not a full safety inspection. I will show why the visible context matters.'),
(20,'Surface marks may be cosmetic, but a cropped photo still needs more views. A visibly flat tire is a clear reason not to drive before assistance. A damaged front area may need inspection. These photos illustrate findings, not confirmed roadworthiness.'),
(25,'This BMW is designed to open its roof. Roof down is not roof damage. The SUV has a visibly crushed roof and damaged windshield. I plan to train and test this difference using both normal designs and real damage. This is a planned test, not a proven result.'),
(30,'There are three answers. Low visible concern means enough clear views show only small or no visible damage. It is not a safety certificate. Do not drive means clear serious visible danger. Inspection required means the photos leave an important question. Each answer gives the visible reason and next step.'),
(30,'The earlier project audit reports thirteen thousand, nine hundred and forty-five VehiDE photo files and over thirty-six thousand marked damage areas. Areas are not extra photos. Thirty-six sample photos have been chosen, with expert action reviews still open. More than twenty thousand useful real photos is a collection goal, not an achieved total.'),
(40,'First, check photo rights, remove copies and group photos of the same car. Second, reviewers record visible damage and the next action. Third, separate training, validation and test cases. Compare a simple image model with a damage detector plus clear action rules. Combine views only if they really belong to one car. Choose settings on validation, freeze them, then run the final test.'),
(30,'For one car, check whether any photos are usable. Find visible damage. A clear serious hazard leads to do not drive, even if other views are missing. Otherwise, incomplete views or an unresolved concern lead to inspection. Only enough clear evidence can support low visible concern.'),
(35,'The main mistake is an expert do-not-drive case predicted low visible concern. I count it out of all expert do-not-drive cases. I also measure all three answers and inspection requests. Sending every car for inspection is not enough to show useful performance. Model tests are not finished, so I cannot promise an accuracy number.'),
(20,'Next, I will finish the review pilot, check data rights, train the models and compare them fairly. Then I will write the seventy-page report. The aim is useful advice from photos, not a replacement for a mechanic. Thank you.')]
assert sum(s for s,_ in main)==250
for i,(secs,words) in enumerate(main):P.slides[i].notes_slide.notes_text_frame.text=f'Target {secs} seconds.\n\n{words}'
# Clarify main vs backup slide numbering without changing old text formatting.
for i,sl in enumerate(P.slides):
 for sh in sl.shapes:
  if sh.has_text_frame and sh.text.isdigit() and sh.left>Inches(12):
   for p in sh.text_frame.paragraphs:
    if p.runs:p.runs[0].text=str(i+1)
output=OUT/'Presentation_Real_Photos_v5.pptx'
with output.open('xb') as f:P.save(f)
(OUT/'photo_manifest.json').write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
sources='# Photo sources and licensing\n\nThese are real licensed presentation illustrations, NOT images acquired from the audited VehiDE/DrBimmer collection. They add zero images to the training or test dataset inventory. Captions are visible-evidence explanations, not expert ground-truth inspection outcomes.\n\n'
for r in records:sources+='## '+r['file']+'\n- Photographer: '+r['author']+'\n- Source: '+r['source']+'\n- License: '+r['license']+' — '+r['license_url']+'\n- Changes: '+r['changes']+'\n\n'
sources+='## Reuse and safeguards\nPhotographs retain their individual licenses; no photographer or manufacturer endorsement is implied. CC BY-SA image derivatives remain available under CC BY-SA 4.0; this is not a blanket relicensing of other components. Presentation use does not establish machine-learning rights for a future dataset. The left surface-detail and right front-damage panels share one Pexels source and are not independent examples. The surface detail is not assigned a whole-car low-concern category: the full source contains other front-area damage.\n\n## Planned design-aware evaluation\nA roof-down convertible must not automatically be labeled roof-damaged. Convertible is not a synonym for undamaged: include damaged convertibles and undamaged fixed-roof cars/SUVs, multiple backgrounds and roof-up/down states. Record design/state separately from damage. Use disjoint vehicles for learning and testing; inspect source shortcuts and roof false alarms/misses. These two comparison pictures do not establish a trained feature, novelty or an error rate.\n'
(OUT/'PHOTO_SOURCES.md').write_text(sources,encoding='utf-8')
doc=Document();doc.add_heading('Real-photo presentation: what to say',0);doc.add_paragraph('Use Presentation_Real_Photos_v5.pptx. Nine main slides, then question-only backups. Target: 4 minutes 10 seconds; rehearse your pace. The printed proposal does not need to be replaced for this slide update.')
for i,(secs,words) in enumerate(main):doc.add_heading(f'Slide {i+1} — {secs} seconds',1);doc.add_paragraph(words)
doc.add_heading('How to explain what makes this example useful',1);doc.add_paragraph('An open roof can be a normal factory feature. The model needs examples of normal designs as well as damage. We will test whether it confuses the two. This is a planned reliability check, not a claim that we invented convertible recognition.')
doc.add_heading('Important limits',1);doc.add_paragraph('These photos are licensed illustrations, not VehiDE training examples. No photo proves that an entire car is roadworthy. The surface-detail crop needs more views. The full front-damage source contains more than superficial marks. All new model tests remain planned.')
with (OUT/'Photo_Presentation_Script_v5.docx').open('xb') as f:doc.save(f)
Q=Presentation(output);assert len(Q.slides)==14
for i,sl in enumerate(Q.slides):
 for sh in sl.shapes:assert sh.left>=0 and sh.top>=0 and sh.left+sh.width<=Q.slide_width+12000 and sh.top+sh.height<=Q.slide_height+12000,(i,sh.name)
print('Verified:',len(Q.slides),'slides; 9 main, 5 backups; 250-second target;',sum(len(t.split()) for _,t in main),'spoken words; embedded real photos with credits.')
# Contact sheets for inspection of the source images actually embedded.
ims=[]
for rec in records:
 im=Image.open(AS/rec['file']);thumb=ImageOps.contain(im,(600,330));canvas=Image.new('RGB',(620,370),'white');canvas.paste(thumb,((620-thumb.width)//2,30));ImageDraw.Draw(canvas).text((10,8),rec['file'],fill='black');ims.append(canvas)
contact=Image.new('RGB',(1240,370*3),'#DCE4EE')
for i,im in enumerate(ims):contact.paste(im,((i%2)*620,(i//2)*370))
contact.save(OUT/'image_check.png')
