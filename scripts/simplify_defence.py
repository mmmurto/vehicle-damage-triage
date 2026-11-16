from pathlib import Path
from pptx import Presentation
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path.cwd();OUT=ROOT/'simple-presentation';OUT.mkdir(exist_ok=True)
P=Presentation(ROOT/'presentation-redesign/Vehicle_Damage_Proposal_Designed_v2.pptx')
updates=[
{1:'BACHELOR PROJECT • FIRST PRESENTATION',7:'Using car photos to suggest the next step',8:'Find the visible damage.\nExplain what to do next.',10:'FIVE-MINUTE PROJECT PLAN',23:'PHOTO → DAMAGE → NEXT STEP',24:'Photos cannot prove\na car is safe to drive.',25:'Working title • final title and name to confirm'},
{1:'01 / WHY THIS PROJECT?',2:'Not all car damage means the same thing.',3:'A small scratch is different from a broken wheel. Some problems cannot be seen in photos.',10:'SMALL DAMAGE',11:'A small scratch on a door',12:'Show and explain the scratch.',16:'CLEAR DANGER',17:'A torn tire or wheel out of place',18:'Ask a mechanic before driving.',22:'NOT CLEAR',23:'A missing view or possible leak',24:'Explain what needs checking.',26:'A photo cannot tell us if the brakes, steering or engine work.'},
{1:'02 / THREE POSSIBLE ANSWERS',2:'Give an answer. Explain the reason.',3:'The answer is based only on what the photos show.',10:'Small surface damage; enough clear views.',11:'The car has not been checked in person.',15:'A clear danger, such as a badly torn tire.',16:'Get a mechanic to check it before driving.',20:'Unclear photos or a problem we cannot judge.',21:'Explain what needs a closer check.',23:'BROKEN GLASS: Where is it? How bad is it? Does it block the driver’s view?'},
{1:'03 / WHAT WE HAVE SO FAR',2:'We have a starting point. More work is needed.',3:'These numbers come from the earlier project check. I have not counted the files again.',9:'VehiDE car photos',12:'Marked damage areas',15:'Photos chosen for a small trial',17:'PHOTO COLLECTION GOAL',18:'More than 20,000 real photos',19:'50,000+ if possible • not collected yet',21:'People still need to review',22:'No confirmed safety-check\nresults found yet.',23:'Check permission. Remove copies. Count photos and known cars separately.'},
{1:'04 / HOW THE SYSTEM WILL WORK',2:'Start simple. Then see what works better.',3:'Test both versions on the same separate test photos.',8:'ADD PHOTOS',9:'Check photo quality\nCheck the views',12:'FIND DAMAGE',13:'Find damaged areas\nUse more views if available',16:'GIVE AN ANSWER',17:'Answer + reason\nWhat to do next',19:'FIRST VERSION',20:'Train a simple model to choose one of the three answers.',21:'The project has tools for checking data. The damage model has not been trained yet.'},
{1:'05 / CHECKING THE PHOTOS',2:'Try a small group before using thousands of photos.',3:'Write down three separate things: visible damage, suggested next step, and any real inspection result.',8:'Small trial → fix problems → add more',10:'36 photos chosen; aim for about 60 cases',12:'Two people review; a car expert helps settle differences',13:'HARD CASES',14:'Glass, tires, wheels, missing views and possible leaks',16:'Keep photos of the same car together',18:'Find copied or very similar photos first.',20:'Use the same car in only one data group.',22:'The same photo time does not prove it is the same car.'},
{1:'06 / HOW WE WILL TEST IT',2:'Avoid missing clear dangers. Still give useful answers.',3:'Choose the settings before the final test. Do not change them to improve the test result.',8:'THE MAIN MISTAKE TO WATCH',9:'Expert says “do not drive” → model says “low concern”',11:'Count this mistake out of all expert “do not drive” cases.',12:'• Count mistakes and explain the limits',13:'• Check how well each of the three answers works',14:'• Count how many cases are sent for inspection',16:'Find a useful balance',21:'MISSED RISKS',23:'MORE CHECKS',24:'Sending every car for a check is not enough.'},
{1:'07 / WHAT HAPPENS NEXT',2:'Step by step: build, test and write the 70-page report.',3:'The exact dates will follow the university deadline.',15:'PREPARE',16:'Get permission\nand review a small sample',21:'Train two versions\nand test them fairly',25:'Explain the results\nand the mistakes',27:'The goal: useful advice from photos—not a promise that a car is safe.'},
{1:'EXTRA SLIDE / FOR QUESTIONS ONLY',2:'Where the current numbers come from',6:'R1 · Earlier project data check: 3482f30',7:'13,945 files; 36,081 marked areas; 7 damage types. Not counted again here.',9:'R2 · Small trial sample',10:'36 photos chosen. People have not finished reviewing them.',12:'Important · Photos of the same car',13:'Matching photo times may suggest a link. They do not prove it is the same car.'},
{1:'EXTRA SLIDE / FOR QUESTIONS ONLY',2:'Possible photo sources: check permission first',7:'Permission from the owners is required. Sharing the photos is restricted.',9:'VehiDE · research and download source',10:'The paper lists 8 damage types; the earlier file check found 7.',13:'Website lists this count. Permission and copied photos still need checking.'}
]
# Preserve all shapes, paragraph styling and runs; replace run text only.
def set_words(sh,words):
 lines=words.split('\n');ps=sh.text_frame.paragraphs
 assert len(lines)<=len(ps),(sh.name,words)
 for i,p in enumerate(ps):
  value=lines[i] if i<len(lines) else ''
  if not p.runs:p.add_run()
  p.runs[0].text=value
  for r in list(p.runs)[1:]:r.text=''
for si,mapping in enumerate(updates):
 sl=P.slides[si]
 for idx,words in mapping.items():set_words(sl.shapes[idx],words)
 for sh in sl.shapes:
  if sh.has_text_frame and sh.text=='VEHICLE DAMAGE TRIAGE  /  PROPOSAL DEFENCE  /  WORKING TITLE':
   set_words(sh,'CAR DAMAGE FROM PHOTOS  /  FIRST PROJECT PRESENTATION  /  WORKING TITLE')
# Complete simple-English talk. Technical category names are retained but explained.
talk=[
('My project',35,'''Good morning. My project is about using photos to look at damage on passenger cars. The system will show the visible damage and suggest what to do next. For example, it may see a small scratch, a badly torn tire, or a problem that is not clear. It will not promise that a car is safe to drive. Today, I will explain my project plan, the photos we have found, and how I will test the system.'''),
('Why this project matters',35,'''Not all car damage is the same. A small scratch on a door may only affect how the car looks. A badly damaged tire is much more serious. Sometimes, the photo does not show enough. There may be a wet patch under the car, but we cannot tell where it came from. Also, a normal-looking car can still have problems with its brakes or steering. That is why the system must explain both what it sees and what it cannot check.'''),
('Three possible answers',45,'''The system will give one of three answers. The first is low visible concern. This means the photos show only small surface damage and give enough clear views for this limited check. It does not mean the car is safe. The second is do not drive. This is for a clear danger, such as a badly torn tire or a wheel that has moved out of place. The third is inspection required. This means a person needs to check the car because the photos are unclear or leave an important question. Broken glass also needs care: where is it, and does it block the driver’s view?'''),
('The photos and current work',45,'''The earlier project check reports thirteen thousand, nine hundred and forty-five photos from a dataset called VehiDE. It also reports over thirty-six thousand marked damage areas. These are areas inside the photos, not extra photos. Thirty-six photos have been chosen for a small trial, but people have not finished reviewing them. My new goal is more than twenty thousand useful real photos, and fifty thousand if possible. Before adding photos, I must check permission and remove copies. So far, we have not found confirmed safety-check results linked to these photos.'''),
('How the system will work',35,'''First, the user adds photos of a car. The system checks whether the photos are clear and show the needed views. A computer model then looks for damage. The final answer gives the category, the visible reason, and the next step. I will start with a simple model that chooses one of the three answers. Then I will test an improved version that finds damaged areas and uses several views of the same car, where those views are available. The model has not been trained yet.'''),
('How people will check the photos',40,'''Before using thousands of photos, I will run a small trial. We already have thirty-six sample photos, and I plan to add more difficult cases. Two people will review the photos separately. A car expert will help when they disagree. We will record the visible damage separately from the suggested next step. We will also look for copied photos. Photos of the same car must stay together, so the model does not learn from a car and then get tested on that same car. A matching photo time alone does not prove that two photos show the same car.'''),
('How I will test it',40,'''The main mistake I want to avoid is this: an expert says do not drive, but the model says low visible concern. I will count how often that happens out of all the expert do-not-drive cases. I will also check all three answers and count how many cars are sent for inspection. Sending every car for inspection is not enough to show that the system is useful. I will choose the settings before the final test, then report the real results, including mistakes and limits. There are no model test results yet.'''),
('Next steps',25,'''Next, I will confirm the university requirements, check photo permissions, and finish the small review trial. Then I will train the models, compare them fairly, and write the seventy-page report. The aim is to give useful, clear advice from visible damage. It is not to replace a mechanic or promise that a car is safe to drive. Thank you.''')]
for i,(name,seconds,speech) in enumerate(talk):
 P.slides[i].notes_slide.notes_text_frame.text=f'Slide {i+1}: {name}\nAim for {seconds} seconds.\n\n{speech}'
for sl in list(P.slides)[8:]:sl.notes_slide.notes_text_frame.text='Extra source slide. Use only if someone asks where the information came from. It is not part of the five-minute talk.'
ppt=OUT/'Car_Damage_Presentation_Simple_English_v3.pptx'
with ppt.open('xb') as f:P.save(f)
D=Document();sec=D.sections[0];sec.top_margin=Inches(.65);sec.bottom_margin=Inches(.65)
D.styles['Normal'].font.name='Calibri';D.styles['Normal'].font.size=Pt(13);D.styles['Normal'].paragraph_format.line_spacing=1.15
for sty in ['Title','Heading 1','Heading 2']:D.styles[sty].font.color.rgb=RGBColor.from_string('152B45')
D.add_heading('My five-minute presentation',0);D.add_paragraph('Simple English • matches the v3 PowerPoint','Subtitle')
D.add_paragraph('Use the eight main slides. The last two slides are only for questions. Read the “What to say” text. You do not need to read the reminders aloud.')
D.add_paragraph('The title is still a working title. Keep your official title if the university has already approved one. The speech explains the plan; it does not claim that the model is finished.')
words=sum(len(t[2].split()) for t in talk)
D.add_paragraph(f'Total time: 5 minutes. About {words} spoken words. Practise slowly with a timer. If you finish early, pause between the slides rather than adding difficult words.')
D.add_heading('Three names you need to know',1)
for a,b in [('Low visible concern','Only small damage can be seen in enough clear views. This does not mean safe to drive.'),('Do not drive','A clear serious danger can be seen. Ask a mechanic before driving.'),('Inspection required','We need clearer photos or a person to check the car.')]:
 D.add_paragraph(a,style='Heading 2');D.add_paragraph(b)
reminders=['Speak slowly. Explain the purpose first.','Use the scratch and tire examples.','Keep the three category names, but explain them in simple words.','Damage areas are not extra photos. The new collection goal has not been reached.','The model is planned, not trained.','The photo sample exists. Expert reviews are not finished.','Describe the mistake you want to avoid. Do not invent a success rate.','End clearly. Thank the teachers.']
elapsed=0
for i,(name,seconds,speech) in enumerate(talk):
 D.add_page_break();D.add_heading(f'Slide {i+1}: {name}',1);elapsed+=seconds
 D.add_paragraph(f'About {seconds} seconds • finish by {elapsed//60}:{elapsed%60:02}','Subtitle')
 D.add_heading('What to say',2);D.add_paragraph(speech)
 D.add_heading('Remember',2);D.add_paragraph(reminders[i])
D.add_page_break();D.add_heading('Simple answers to likely questions',1)
qa=[('Can your system say a car is safe?','No. It only gives advice from what the photos show. A mechanic must check things that photos cannot show.'),('How many photos do you have?','The earlier project check reports 13,945 VehiDE photos. I still need to check copies and useful coverage before giving a final total.'),('Is the system finished?','No. We have research documents, data-checking tools and a small photo sample. Model training and testing are still planned.'),('Why do you want more photos?','I need different damage types and clear examples of serious problems. More photos only help if they are useful and not copies.'),('How will you test it?','I will compare its answers with expert reviews on photos not used for training. I will report mistakes and how often it asks for inspection.'),('Why not send every car for inspection?','That avoids many low-concern mistakes, but it does not give much useful help. I need to show both the mistakes and the number of inspection requests.'),('What does triage mean?','It means making a first decision about what should happen next. It is not a full inspection.'),('What if you cannot find real inspection records?','Then I will test agreement with expert photo reviews. I will not claim to measure actual road safety.')]
for q,a in qa:D.add_heading(q,2);D.add_paragraph(a)
sec.header.paragraphs[0].text='CAR DAMAGE PROJECT | SIMPLE SPEAKING SCRIPT'
f=sec.footer.paragraphs[0];f.text='Practise slowly • Page ';field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');f._p.append(field)
word=OUT/'Five_Minute_Script_Simple_English_v3.docx'
with word.open('xb') as f:D.save(f)
Q=Presentation(ppt);assert len(Q.slides)==10;assert sum(t[1] for t in talk)==300
assert len(Document(word).paragraphs)>40
for a,b in zip(P.slides,Q.slides):
 assert len(a.shapes)==len(b.shapes)
 for sh in b.shapes:assert sh.left>=0 and sh.top>=0 and sh.left+sh.width<=Q.slide_width+15000 and sh.top+sh.height<=Q.slide_height+15000
print(f'Checked 8 main slides + 2 backup slides; 300 seconds; {words} spoken words. Layout retained; text and notes simplified.');print(ppt);print(word)
