# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.2.4
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x00\xa1\
<\
\xb8d\x18\xca\xef\x9c\x95\xcd!\x1c\xbf`\xa1\xbd\xdd\xa7\
\x00\x00\x00\x02deB\x00\x00\x00\x10\x00*\xd0%\x00\
\x00\x00\x00\x03J\xc1q\x00\x00\x00.i\x00\x00\x00i\
\x03\x00\x00\x00\x0a\x00D\x00a\x00t\x00e\x00i\x08\
\x00\x00\x00\x00\x06\x00\x00\x00\x05&File\x07\x00\
\x00\x00\x0aMainWindow\x01\x03\x00\
\x00\x00\x16\x00H\x00a\x00l\x00l\x00o\x00 \x00\
W\x00e\x00l\x00t\x00!\x08\x00\x00\x00\x00\x06\x00\
\x00\x00\x0cHello world!\x07\
\x00\x00\x00\x04main\x01\x88\x00\x00\x00\x02\x01\x01\
\
\x00\x00\x03U\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0afunc\
tion toggleMaxim\
ized() {\x0a    if \
(appWindow.visib\
ility === Window\
.Maximized) {\x0a  \
      appWindow.\
showNormal()\x0a   \
 } else {\x0a      \
  appWindow.show\
Maximized()\x0a    \
}\x0a}\x0a\
\x00\x00\x06\x97\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport compon\
ents\x0aimport hand\
lers\x0aimport pyob\
jects\x0aimport \x22wi\
ndow-operations.\
js\x22 as WindowOpe\
rations\x0a\x0a\x0aApplic\
ationWindow {\x0a  \
  id: window\x0a\x0a  \
  property Appli\
cationWindow app\
Window: window\x0a \
   property var \
windowOperations\
: WindowOperatio\
ns\x0a    property \
var appTheme: Se\
ttingsPyObject.t\
heme\x0a    propert\
y var appThemeCo\
lorAccent: Setti\
ngsPyObject.them\
e_accent\x0a    pro\
perty int window\
Border: 5\x0a\x0a    v\
isible: true\x0a   \
 width: 1290\x0a   \
 height: 970\x0a   \
 flags: Qt.Frame\
lessWindowHint\x0a\x0a\
    Material.the\
me: appTheme\x0a   \
 Material.accent\
: appThemeColorA\
ccent\x0a\x0a    Layou\
tMirroring.enabl\
ed: TranslationP\
yObject.rtl_enab\
led\x0a    LayoutMi\
rroring.children\
Inherit: true\x0a\x0a \
   WindowBorderM\
ouseCurser {\x0a\x0a  \
      borderWidt\
h: windowBorder\x0a\
        anchors.\
fill: parent\x0a\x0a  \
  }\x0a\x0a    WindowR\
esizeHandler {\x0a\x0a\
        borderWi\
dth: windowBorde\
r\x0a\x0a    }\x0a\x0a    Pa\
geMain {\x0a\x0a      \
  anchors.fill: \
parent\x0a        a\
nchors.margins: \
appWindow.visibi\
lity === Window.\
Windowed ? windo\
wBorder : 0\x0a\x0a   \
 }\x0a\x0a}\x0a\
\x00\x00\x00p\
m\
odule handlers\x0aW\
indowBorderMouse\
Curser WindowBor\
derMouseCurser.q\
ml\x0aWindowResizeH\
andler WindowRes\
izeHandler.qml\x0a\
\x00\x00\x05b\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0a\x0a\x0aMou\
seArea {\x0a\x0a    pr\
operty int borde\
rWidth\x0a\x0a    hove\
rEnabled: true\x0a \
   acceptedButto\
ns: Qt.NoButton \
// don't actuall\
y handle events\x0a\
\x0a    cursorShape\
: {\x0a        cons\
t p = Qt.point(m\
ouseX, mouseY)\x0a \
       const b =\
 borderWidth + 1\
5 // Increase th\
e corner size sl\
ightly\x0a        i\
f (p.x < b && p.\
y < b) return Qt\
.SizeFDiagCursor\
\x0a        if (p.x\
 >= width - b &&\
 p.y >= height -\
 b) return Qt.Si\
zeFDiagCursor\x0a  \
      if (p.x >=\
 width - b && p.\
y < b) return Qt\
.SizeBDiagCursor\
\x0a        if (p.x\
 < b && p.y >= h\
eight - b) retur\
n Qt.SizeBDiagCu\
rsor\x0a        if \
(p.x < b || p.x \
>= width - b) re\
turn Qt.SizeHorC\
ursor\x0a        if\
 (p.y < b || p.y\
 >= height - b) \
return Qt.SizeVe\
rCursor\x0a    }\x0a\x0a}\
\x0a\
\x00\x00\x04\xf2\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0a\x0a\x0aDra\
gHandler {\x0a\x0a    \
property int bor\
derWidth\x0a\x0a    gr\
abPermissions: T\
apHandler.TakeOv\
erForbidden\x0a\x0a   \
 target: null\x0a\x0a \
   onActiveChang\
ed: {\x0a        if\
 (active) {\x0a    \
        const p \
= centroid.posit\
ion\x0a            \
const b = border\
Width + 15 // In\
crease the corne\
r size slightly\x0a\
            let \
e = 0\x0a          \
  if (p.x < b) {\
 e |= Qt.LeftEdg\
e }\x0a            \
if (p.x >= width\
 - b) { e |= Qt.\
RightEdge }\x0a    \
        if (p.y \
< b) { e |= Qt.T\
opEdge }\x0a       \
     if (p.y >= \
height - b) { e \
|= Qt.BottomEdge\
 }\x0a            a\
ppWindow.startSy\
stemResize(e)\x0a  \
      }\x0a    }\x0a\x0a}\
\x0a\
\x00\x00\x00\xd2\
m\
odule models\x0aAcc\
entColorModel Ac\
centColorModel.q\
ml\x0aArtworkModel \
ArtworkModel.qml\
\x0aDeveloperModel \
DeveloperModel.q\
ml\x0aDependencyMod\
el DependencyMod\
el.qml\x0aLanguageM\
odel LanguageMod\
el.qml\x0aThemeMode\
l ThemeModel.qml\
\x0a\
\x00\x00\x07M\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls.Material\x0a\x0a\x0aLi\
stModel {\x0a    Li\
stElement { acce\
ntColor: 0   /* \
Material.Red */ \
}\x0a    ListElemen\
t { accentColor:\
 1   /* Material\
.Pink */ }\x0a    L\
istElement { acc\
entColor: 2   /*\
 Material.Purple\
 */ }\x0a    ListEl\
ement { accentCo\
lor: 3   /* Mate\
rial.DeepPurple \
*/ }\x0a    ListEle\
ment { accentCol\
or: 4   /* Mater\
ial.Indigo */ }\x0a\
    ListElement \
{ accentColor: 5\
   /* Material.B\
lue */ }\x0a    Lis\
tElement { accen\
tColor: 6   /* M\
aterial.LightBlu\
e */ }\x0a    ListE\
lement { accentC\
olor: 7   /* Mat\
erial.Cyan */ }\x0a\
    ListElement \
{ accentColor: 8\
   /* Material.T\
eal */ }\x0a    Lis\
tElement { accen\
tColor: 9   /* M\
aterial.Green */\
 }\x0a    ListEleme\
nt { accentColor\
: 10  /* Materia\
l.LightGreen */ \
}\x0a    ListElemen\
t { accentColor:\
 11  /* Material\
.Lime */ }\x0a    L\
istElement { acc\
entColor: 12  /*\
 Material.Yellow\
 */ }\x0a    ListEl\
ement { accentCo\
lor: 13  /* Mate\
rial.Amber */ }\x0a\
    ListElement \
{ accentColor: 1\
4  /* Material.O\
range */ }\x0a    L\
istElement { acc\
entColor: 15  /*\
 Material.DeepOr\
ange */ }\x0a    Li\
stElement { acce\
ntColor: 16  /* \
Material.Brown *\
/ }\x0a    ListElem\
ent { accentColo\
r: 17  /* Materi\
al.Grey */ }\x0a   \
 ListElement { a\
ccentColor: 18  \
/* Material.Blue\
Grey */ }\x0a}\x0a\
\x00\x00\x03,\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0a\x0a\x0aLis\
tModel {\x0a    Lis\
tElement {\x0a     \
   name: \x22Frechd\
achs\x22\x0a    }\x0a    \
ListElement {\x0a  \
      name: \x22tri\
n\x22\x0a    }\x0a}\x0a\
\x00\x00\x05\xc6\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0a\x0a\x0aLis\
tModel {\x0a\x0a    pr\
operty var langu\
agesForTranslati\
onTool: [\x0a      \
  qsTranslate(\x22L\
anguages\x22, \x22Engl\
ish\x22),\x0a        q\
sTranslate(\x22Lang\
uages\x22, \x22German\x22\
),\x0a        qsTra\
nslate(\x22Language\
s\x22, \x22Hebrew\x22),\x0a \
       qsTransla\
te(\x22Languages\x22, \
\x22Italian\x22),\x0a    \
    qsTranslate(\
\x22Languages\x22, \x22Sp\
anish\x22),\x0a    ]\x0a\x0a\
    ListElement \
{\x0a        langua\
ge: \x22English\x22\x0a  \
      abbrev: \x22e\
n\x22\x0a    }\x0a    Lis\
tElement {\x0a     \
   language: \x22Ge\
rman\x22\x0a        ab\
brev: \x22de\x22\x0a     \
   translator: \x22\
Frechdachs\x22\x0a    \
}\x0a    ListElemen\
t {\x0a        lang\
uage: \x22Hebrew\x22\x0a \
       abbrev: \x22\
he\x22\x0a        tran\
slator: \x22cN3rd\x22\x0a\
    }\x0a    ListEl\
ement {\x0a        \
language: \x22Itali\
an\x22\x0a        abbr\
ev: \x22it\x22\x0a       \
 translator: \x22ma\
ddo\x22\x0a    }\x0a    L\
istElement {\x0a   \
     language: \x22\
Spanish\x22\x0a       \
 abbrev: \x22es\x22\x0a  \
      translator\
: \x22RcUchiha\x22\x0a   \
 }\x0a}\x0a\
\x00\x00\x02\xfd\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0a\x0a\x0aLis\
tModel {\x0a    Lis\
tElement {\x0a     \
   name: \x22maleun\
am\x22\x0a    }\x0a}\x0a\
\x00\x00\x05\xd3\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0a\x0a\x0aLis\
tModel {\x0a    Lis\
tElement {\x0a     \
   name: \x22mpv\x22\x0a \
       url: \x22htt\
ps://mpv.io/\x22\x0a  \
      licence: \x22\
GPL-2.0+\x22\x0a    }\x0a\
    ListElement \
{\x0a        name: \
\x22libmpv\x22\x0a       \
 url: \x22https://m\
pv.io/installati\
on/\x22\x0a        lic\
ence: \x22GPL-3.0\x22\x0a\
    }\x0a    ListEl\
ement {\x0a        \
name: \x22python-mp\
v\x22\x0a        url: \
\x22https://github.\
com/jaseg/python\
-mpv\x22\x0a        li\
cence: \x22AGPL-3.0\
\x22\x0a    }\x0a    List\
Element {\x0a      \
  name: \x22PySide6\
\x22\x0a        url: \x22\
https://wiki.qt.\
io/Qt_for_Python\
\x22\x0a        licenc\
e: \x22LGPL-3.0\x22\x0a  \
  }\x0a    ListElem\
ent {\x0a        na\
me: \x22python-inje\
ct\x22\x0a        url:\
 \x22https://github\
.com/ivankorobko\
v/python-inject\x22\
\x0a        licence\
: \x22Apache-2.0\x22\x0a \
   }\x0a    ListEle\
ment {\x0a        n\
ame: \x22material-d\
esign-icons\x22\x0a   \
     url: \x22https\
://github.com/go\
ogle/material-de\
sign-icons\x22\x0a    \
    licence: \x22Ap\
ache-2.0\x22\x0a    }\x0a\
}\x0a\
\x00\x00\x03@\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls.Material\x0a\x0a\x0aLi\
stModel {\x0a    Li\
stElement { them\
e: Material.Ligh\
t }\x0a    ListElem\
ent { theme: Mat\
erial.Dark }\x0a}\x0a\
\x00\x00\x00S\
m\
odule helpers\x0asi\
ngleton CommentT\
ypeWidthCalculat\
or CommentTypeWi\
dthCalculator.qm\
l\x0a\
\x00\x00\x06o\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aprag\
ma Singleton\x0aimp\
ort QtQuick\x0aimpo\
rt pyobjects\x0a\x0a\x0aQ\
tObject {\x0a\x0a    i\
d: object\x0a\x0a    p\
roperty var comm\
entTypesDefined:\
 SettingsPyObjec\
t.comment_types\x0a\
    property var\
 commentTypesImp\
orted: [\x22Hallo\x22,\
 \x22helloHello\x22]\x0a\x0a\
    property var\
 widthCommentTyp\
esDefined: 0\x0a   \
 property var wi\
dthCommentTypesI\
mported: 0\x0a\x0a    \
property var wid\
th: Math.max(wid\
thCommentTypesDe\
fined, widthComm\
entTypesImported\
)\x0a\x0a    onComment\
TypesDefinedChan\
ged: calculateMa\
xWidthOf(comment\
TypesDefined)\x0a  \
  onCommentTypes\
ImportedChanged:\
 calculateMaxWid\
thOf(commentType\
sImported)\x0a\x0a    \
function calcula\
teMaxWidthOf(ele\
ments) {\x0a       \
 const metric = \
Qt.createQmlObje\
ct('import QtQui\
ck; TextMetrics \
{}', object)\x0a   \
     let width =\
 0\x0a        for (\
let element of e\
lements) {\x0a     \
       metric.te\
xt = qsTranslate\
(\x22CommentTypes\x22,\
 element)\x0a      \
      width = Ma\
th.max(width, me\
tric.tightBoundi\
ngRect.width)\x0a  \
      }\x0a        \
metric.destroy()\
\x0a        object.\
widthCommentType\
sDefined = width\
 + 6\x0a    }\x0a\x0a}\x0a\
\x00\x00\x07R\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Contr\
ols\x0a\x0a\x0aMenuAutoWi\
dth {\x0a\x0a    title\
: qsTranslate(\x22M\
ainWindow\x22, \x22&Fi\
le\x22)\x0a\x0a    Action\
 {\x0a        text:\
 qsTranslate(\x22Ma\
inWindow\x22, \x22&New\
 QC Document\x22)\x0a \
       shortcut:\
 \x22CTRL+N\x22\x0a      \
  onTriggered: {\
\x0a            con\
sole.log(\x22New QC\
 Document\x22)\x0a    \
    }\x0a    }\x0a\x0a   \
 Action {\x0a      \
  text: qsTransl\
ate(\x22MainWindow\x22\
, \x22&Open QC Docu\
ment(s)...\x22)\x0a   \
     shortcut: \x22\
CTRL+O\x22\x0a        \
onTriggered: {\x0a \
           const\
 component = Qt.\
createComponent(\
\x22qrc:/qml/compon\
ents/DialogOpenD\
ocuments.qml\x22)\x0a \
           const\
 dialog = compon\
ent.createObject\
(appWindow)\x0a    \
        dialog.o\
pen()\x0a        }\x0a\
    }\x0a\x0a    Actio\
n {\x0a        text\
: qsTranslate(\x22M\
ainWindow\x22, \x22&Sa\
ve QC Document\x22)\
\x0a        shortcu\
t: \x22CTRL+S\x22\x0a    \
    onTriggered:\
 {\x0a            c\
onsole.log(\x22Save\
 QC Document\x22)\x0a \
       }\x0a    }\x0a\x0a\
    Action {\x0a   \
     text: qsTra\
nslate(\x22MainWind\
ow\x22, \x22&Save QC D\
ocument As...\x22)\x0a\
        shortcut\
: \x22CTRL+Shift+S\x22\
\x0a        onTrigg\
ered: {\x0a        \
    console.log(\
\x22Save QC Documen\
t As...\x22)\x0a      \
  }\x0a    }\x0a\x0a    M\
enuSeparator { }\
\x0a\x0a    Action {\x0a \
       text: qsT\
ranslate(\x22MainWi\
ndow\x22, \x22&Exit mp\
vQC\x22)\x0a        sh\
ortcut: \x22CTRL+Q\x22\
\x0a        onTrigg\
ered: {\x0a        \
    console.log(\
\x22Exit mpvQC\x22)\x0a  \
      }\x0a    }\x0a\x0a}\
\x0a\
\x00\x00\x04\xc8\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Dialo\
gs\x0aimport pyobje\
cts\x0a\x0a\x0aFileDialog\
 {\x0a\x0a    title: q\
sTranslate(\x22File\
InteractionDialo\
gs\x22, \x22Open Video\
\x22)\x0a    currentFo\
lder: SettingsPy\
Object.import_la\
st_dir_video\x0a\x0a  \
  nameFilters: [\
\x0a        qsTrans\
late(\x22FileIntera\
ctionDialogs\x22, \x22\
Video files\x22) + \
\x22 (*.mp4 *.mkv *\
.avi)\x22,\x0a        \
qsTranslate(\x22Fil\
eInteractionDial\
ogs\x22, \x22All files\
\x22) + \x22 (*.*)\x22,\x0a \
   ]\x0a\x0a    onAcce\
pted: {\x0a        \
SettingsPyObject\
.import_last_dir\
_video = current\
Folder.toString(\
)\x0a        QcMana\
gerPyObject.open\
_video(currentFi\
le)\x0a    }\x0a\x0a    o\
nRejected: {\x0a\x0a  \
  }\x0a\x0a}\x0a\
\x00\x00\x04*\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Contr\
ols\x0a\x0a\x0aToolButton\
 {\x0a\x0a    property\
 bool maximized\x0a\
\x0a    property ur\
l iconMaximize: \
\x22qrc:/data/icons\
/open_in_full_bl\
ack_24dp.svg\x22\x0a  \
  property url i\
conNormalize: \x22q\
rc:/data/icons/c\
lose_fullscreen_\
black_24dp.svg\x22\x0a\
\x0a    icon.source\
: maximized ? ic\
onNormalize : ic\
onMaximize\x0a\x0a    \
icon.width: 18\x0a \
   icon.height: \
18\x0a\x0a    onClicke\
d: windowOperati\
ons.toggleMaximi\
zed()\x0a\x0a}\x0a\
\x00\x00\x04o\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0a\x0a\x0aIte\
m {\x0a\x0a    width: \
parent.width\x0a   \
 height: headerB\
ar.height\x0a\x0a    T\
apHandler {\x0a    \
    onTapped: if\
 (tapCount === 2\
) windowOperatio\
ns.toggleMaximiz\
ed()\x0a        ges\
turePolicy: TapH\
andler.DragThres\
hold\x0a    }\x0a\x0a    \
DragHandler {\x0a  \
      target: nu\
ll\x0a        grabP\
ermissions: TapH\
andler.CanTakeOv\
erFromAnything\x0a \
       onActiveC\
hanged: if (acti\
ve) { window.sta\
rtSystemMove() }\
\x0a    }\x0a\x0a    Head\
erBarContent {\x0a \
       id: heade\
rBar\x0a    }\x0a\x0a}\x0a\
\x00\x00\x03\xac\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport pyobje\
cts\x0a\x0a\x0aLabel {\x0a\x0a \
   id: label\x0a\x0a  \
  property strin\
g comment\x0a\x0a    t\
ext: label.comme\
nt\x0a    horizonta\
lAlignment: Text\
.AlignLeft\x0a    e\
lide: Translatio\
nPyObject.rtl_en\
abled ? Text.Eli\
deLeft: Text.Eli\
deRight\x0a\x0a}\x0a\
\x00\x00\x03V\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Contr\
ols\x0a\x0a\x0aToolButton\
 {\x0a\x0a    icon.sou\
rce: \x22qrc:/data/\
icons/close_blac\
k_24dp.svg\x22\x0a    \
icon.width: 18\x0a \
   icon.height: \
18\x0a\x0a    onClicke\
d: window.close(\
)\x0a\x0a}\x0a\
\x00\x00\x03\xa6\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport pyobje\
cts\x0a\x0a\x0aLabel {\x0a\x0a \
   id: label\x0a\x0a  \
  property strin\
g type\x0a\x0a    text\
: label.type\x0a   \
 horizontalAlign\
ment: Text.Align\
Left\x0a    elide: \
TranslationPyObj\
ect.rtl_enabled \
? Text.ElideLeft\
: Text.ElideRigh\
t\x0a\x0a}\x0a\
\x00\x00\x03K\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0a\x0a\x0aLabel {\x0a\x0a  \
  id: label\x0a\x0a   \
 property string\
 time\x0a\x0a    text:\
 label.time\x0a    \
horizontalAlignm\
ent: Text.AlignH\
Center\x0a\x0a}\x0a\
\x00\x00\x07\x06\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport QtQuic\
k.Layouts\x0aimport\
 helpers\x0a\x0a\x0aItem \
{\x0a\x0a    id: curre\
nt\x0a\x0a    property\
 var index\x0a    p\
roperty var time\
Int\x0a    property\
 var timeStr\x0a   \
 property var ty\
pe\x0a    property \
var comment\x0a\x0a   \
 width: parent.w\
idth\x0a    height:\
 40\x0a\x0a    RowLayo\
ut {\x0a\x0a        wi\
dth: parent.widt\
h\x0a        spacin\
g: 0\x0a\x0a        Bu\
ttonPlay {\x0a     \
       time: cur\
rent.timeInt\x0a   \
     }\x0a\x0a        \
LabelTime {\x0a    \
        time: cu\
rrent.timeStr\x0a  \
          Layout\
.minimumWidth: 1\
00\x0a            L\
ayout.maximumWid\
th: 100\x0a        \
}\x0a\x0a        Label\
Type {\x0a         \
   text: current\
.type\x0a          \
  Layout.minimum\
Width: CommentTy\
peWidthCalculato\
r.width\x0a        \
    Layout.maxim\
umWidth: Comment\
TypeWidthCalcula\
tor.width\x0a      \
  }\x0a\x0a        Lab\
elComment {\x0a    \
        comment:\
 current.comment\
\x0a            Lay\
out.fillWidth: p\
arent\x0a        }\x0a\
\x0a        ButtonM\
ore {\x0a          \
  id: button\x0a   \
         propert\
y var index: cur\
rent.index\x0a\x0a    \
        onClicke\
d: {\x0a           \
     listView.mo\
del.removeRow(bu\
tton.index)\x0a    \
        }\x0a\x0a     \
   }\x0a\x0a        It\
em {\x0a           \
 width: 16\x0a     \
       height: 0\
\x0a        }\x0a\x0a    \
}\x0a\x0a}\x0a\
\x00\x00\x05E\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport Qt.lab\
s.settings\x0aimpor\
t pyobjects\x0a\x0a\x0aSp\
litView {\x0a\x0a    i\
d: splitView\x0a\x0a  \
  orientation: Q\
t.Vertical\x0a\x0a    \
Settings {\x0a     \
   id: settings\x0a\
        fileName\
: SettingsPyObje\
ct.backing_objec\
t_file_name\x0a    \
    category: \x22S\
plitView\x22\x0a    }\x0a\
\x0a    Item {\x0a    \
    SplitView.fi\
llHeight: true\x0a \
       Player {}\
\x0a    }\x0a\x0a    Item\
 {\x0a        Split\
View.preferredHe\
ight: window.hei\
ght / 5\x0a        \
Component.onComp\
leted: splitView\
.restoreState(se\
ttings.value(\x22di\
mensions\x22))\x0a    \
    Component.on\
Destruction: set\
tings.setValue(\x22\
dimensions\x22, spl\
itView.saveState\
())\x0a\x0a        Lis\
tViewComments {\x0a\
            anch\
ors.fill: parent\
\x0a        }\x0a    }\
\x0a\x0a}\x0a\
\x00\x00\x04\x05\
\x00\
\x00\x0e\x10x\x9c\xedW]O\xe38\x14}\xf7\xaf\xb8\
\xea\xcbP\x06\xa5\xc0j^\x0a\x83\x94)0T*P\
\xda\xb0\x08i^\xdc\xe4\xa6\xb1p\xed\xac\xed\xb4d\x10\
\xff}\xaf\x13\xdaN\xa7av\xa5\x9d\xd1\xb2\xd2\xe6\xa1\
\x8d}?|\xee9\xd7\xae\xdb\xd9e\xb3|~\xd3c\
\xac\xa7\xf3\xd2\x88i\xe6`\xa7\xd7\x86\xc3\xfd\xc3C\xa8\
,\x90\xe0\x1c\xa5\xce\xd1X\xc6\xa2LX\xc8\x8d\x9e\x1a\
>\x03zM\x0d\x22X\x9d\xba\x057\xd8\x85R\x17\x10\
s\x05\x06\x13a\x9d\x11\x93\xc2!\x08\x07\x5c%\x1dm\
`\xa6\x13\x91\x96\x8c&\x0a\x95\xa0\x01\x97!843\
\x0b:\xad\x06\x9f\xafn!LS4\x1a>\xa3B\xc3\
%\x0c\x8b\x89\x141\x0cD\x8c\xca\x22pZ\xde\xcf\xd8\
\x0c\x13\x98\x94\xccG\x9d{\x10\xe3\x17\x10p\xae)9\
wB\xab=@Av\x03s\xc2Nc\xf8m\xb9\xce\
K\xb6=\xd0\x86\xedp\xe7q\x1b\xd0\xb9\x0fj\x13\xd8\
\x12$w\xeb\xb8`\xbb\xeeuy\x09\x08U\xe5\xcc\x88\
\x22z\xa1lT\xdfBH\x09\x13\x84\xc2bZ\xc8=\
F\x9ep\xd7\x8f.\xaeo#\x08\xaf\xee\xe1.\x1c\x8d\
\xc2\xab\xe8\xfe\x88<]\xa6\xc9J$\xd7y\xc4,\x97\
\x82\xd2R1\x86+W\x12fvy6\xea]\x90\x7f\
\xf8\xa9?\xe8G\xf7\x04\x1b\xce\xfb\xd1\xd5\xd9x\x0c\xe7\
\xd7#\x08a\x18\x8e\xa2~\xefv\x10\x8e`x;\x1a\
^\x8f\xcf\x02\x801z@\xc8\xfe\x9a\xd5\xb4\x12\x87\xc8\
K\xd0q!-U|ORZB&\x13\xc8\xf8\x1c\
I\xd2\x18\xc5\x9cpq\x88\xa9S\xfe\xb6b\x8cK\xad\
\xa6U\x99\x14\xb0f\x91\xf0\xf5SP\xda\xed\x81%\x9c\
\xc7\x99sy\xb7\xd3Y,\x16\xc1T\x15\x816\xd3\x8e\
\xac3\xd8\xceI\xc0v;\x8c1\xa2F\x1b\x077\xee\
\xa6\x10\xf1\xc3w\xc3\xa0\xa7\x953Z\xda\xe5<u\x1b\
\xd2\x88\xb1qL\xd3\xf2w\x81\x0bxb\x0c\xe8\x11I\
\x17b\xdf\xa4\xceF|RM-D\xe2\xb2.\xe4\xd4\
B\xca\x05\xd5\xa8\xf6\x8d)-M\xdd\xbdf\xefiY\
\xcc\x14e\x86\x97\xa7)\xd3\xd2\xe6t>\xe4I\x22\xd4\
\xb4\x0b\x07\x1f\xd8j~\xc0'(\xbf\xc9\xe1\x1f\xae\xe2\
L\x1b\x1b\xd0\x87\xf8J \xb8\xecQB4\xab\xd4\xdf\
\x1b6\xa2\x1d>\xba.\xb4N\xeb\xcd;#\x87\xd6\x86\
=\xa5\xc0`\xa2%1\xe1L\x81\xdb\xb6\x5c<\xa2\x1c\
\x8b\xaf\xb4\xado\x5c\xc0s\xea\xca\xb8\xdaV\xc1\xa6\x19\
v\xe1 8\xd8_%x^W5\xc2\x1c\xab\x8d\xb4\
YX%L\x17N\x97\xe7\xca\xa5\x1f\xc3\xd3\xf3\x86\xd3\
\xabz\xfc\x88\xb2\x7fN\xdb\x9a:\xc5g\x9b\xac<7\
\x97\x18;\xae\xa6\x12\xe1\x89:EjZ\xa6\xe5h\xdf\
\xdaz\xb1\xd6\x11d\xe8\x0fU/\xf7\xd1\xb2\xa8\x83\xfd\
oS\xfc2\xedC\xe3\x16\xda<\xbc5\xdd_`\xfd\
\xaf\xfa\xafQ=\xf28d\xa5\xd8[S~@\x9c\x15\
|\x8a?W\xfa\xb9\xb0b\x22\xd1WUW\xae\xb7\xc5\
\xfdY\xed\xb1^\x02\xdeC\x0bvZ\xf4\xf5\x87]R\
\x8e;\xade\x89c\x94\xd4#^\x83=\xbaL\xd4s\
m\x1f\xd3n\xfd\xb7\xdb\xeb\x94\x14\xa6\xcb\x9b\x8a\x05\xda\
\xb7\xd6_+l\xe5\xbf}\xb8\xbc\xd2>-\xba\xe6\xcc\
\xe4\xc9\xb1u%\x89\xeb\xca\x1c?~y\xe7M\x9d\xd8\
\xda/\xefN\x8e;\x95\xe5d+\xfc\x98Cf0%\
o\xdfq\x85\x91\xbe\x95(\xa0\xb5\xe5I\x06\x7f\x86\xad\
\xdb\xb3\xbaE\xc5\xd5D{;o\x87\xd3\xa2\x15\xa8\xed\
TZ\x0d\x84z\x08\xa9\x8d\xe7\xc4yR\xa9F\xbf\xd7\
\xea\xd6\xc8\xb3G\xaaRq)\xcb\x1d\x02\xd3\xde\xae\xf7\
R\xd3\xd574\xc8\x1b\xe8\xf4\x8f\xbf\x81\xcd\x96>\x8d\
\x1eK\xd2S\xbaJ/\x89nv\x8cc\xcc\x09\xdf\xa7\
\xc29\xadl\x05\xf3J\xd7\xa3\xc6\x80\xb80V\x9bq\
\xc6\xf3\xba\x13\x87Z(GW\xb2\x0b\xfa\x9b\xd2\xabl\
\x8da\x99\xa6\xff\x03g\x8a\xd3Y\xd3\xd4\xe2\xfey\xde\
&\x22\xd2ZF\x22\x7f\x85\x86\xba-\x88\xc2F+\xf5\
0/\xbb\xf0a\x7f\xbf\xd1\xbc:\xf8VD\x06\xfe\xb2\
\xca\x85\xb2\x15\xfd\x0d\xf0\x9aG\xf5\x1b\x81\x7ff\x7f\x02\
\xd50\x02\xd6\
\x00\x00\x05\x92\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Contr\
ols\x0aimport QtQui\
ck.Layouts\x0a\x0a\x0aDia\
log {\x0a    width:\
 420\x0a    height:\
 500\x0a\x0a    modal:\
 true\x0a    anchor\
s.centerIn: pare\
nt\x0a    standardB\
uttons: Dialog.O\
k\x0a    closePolic\
y: Popup.CloseOn\
Escape\x0a\x0a    cont\
entItem: ColumnL\
ayout {\x0a        \
width: parent.wi\
dth\x0a\x0a        Tab\
Bar {\x0a          \
  id: bar\x0a      \
      contentWid\
th: parent.width\
\x0a\x0a            Ta\
bButton {\x0a      \
          text: \
qsTranslate(\x22Abo\
utDialog\x22, \x22Abou\
t\x22)\x0a            \
}\x0a\x0a            T\
abButton {\x0a     \
           text:\
 qsTranslate(\x22Ab\
outDialog\x22, \x22Cre\
dits\x22)\x0a         \
   }\x0a        }\x0a\x0a\
        StackLay\
out {\x0a          \
  currentIndex: \
bar.currentIndex\
\x0a            wid\
th: parent.width\
\x0a\x0a            Di\
alogAboutViewAbo\
ut { }\x0a\x0a        \
    DialogAboutV\
iewCredits { }\x0a \
       }\x0a    }\x0a}\
\x0a\
\x00\x00\x06A\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport QtQuic\
k.Layouts\x0aimport\
 models\x0aimport p\
yobjects\x0a\x0a\x0aListV\
iew {\x0a\x0a    id: l\
istViewTheme\x0a\x0a  \
  property int i\
temBorder: 12\x0a\x0a \
   model: ThemeM\
odel {}\x0a    clip\
: true\x0a    spaci\
ng: 8\x0a    height\
: 52\x0a    orienta\
tion: ListView.H\
orizontal\x0a\x0a    d\
elegate: Compone\
nt {\x0a\x0a        Ci\
rcle {\x0a\x0a        \
    width: 52\x0a  \
          height\
: width\x0a        \
    color: appTh\
eme === theme ? \
Material.foregro\
und : \x22transpare\
nt\x22\x0a\x0a           \
 Circle {\x0a\x0a     \
           width\
: parent.width -\
 listViewTheme.i\
temBorder\x0a      \
          height\
: width\x0a        \
        anchors.\
centerIn: parent\
\x0a               \
 color: Material\
.background\x0a\x0a   \
             Mat\
erial.theme: the\
me\x0a\x0a            \
    onClicked: {\
\x0a               \
     appWindow.a\
ppTheme = theme\x0a\
                \
    SettingsPyOb\
ject.theme = the\
me\x0a             \
       listViewT\
heme.currentInde\
x = theme\x0a      \
          }\x0a\x0a   \
         }\x0a\x0a    \
    }\x0a\x0a    }\x0a\x0a}\x0a\
\
\x00\x00\x07$\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport models\
\x0aimport pyobject\
s\x0a\x0a\x0aMenuAutoWidt\
h {\x0a\x0a    title: \
qsTranslate(\x22Mai\
nWindow\x22, \x22&Opti\
ons\x22)\x0a\x0a    MenuA\
utoWidth {\x0a     \
   title: qsTran\
slate(\x22MainWindo\
w\x22, \x22&Language\x22)\
\x0a\x0a        Repeat\
er {\x0a           \
 model: Language\
Model {}\x0a       \
     MenuItem {\x0a\
                \
text: qsTranslat\
e(\x22Translation\x22,\
 model.language)\
\x0a               \
 autoExclusive: \
true\x0a           \
     checkable: \
true\x0a           \
     checked: mo\
del.abbrev === S\
ettingsPyObject.\
language\x0a       \
         onTrigg\
ered: changeLang\
uageTimer.start(\
)\x0a              \
  Timer {\x0a      \
              //\
 Delay it so pos\
sible animations\
 have time\x0a     \
               i\
d: changeLanguag\
eTimer\x0a         \
           inter\
val: 125\x0a       \
             onT\
riggered: Transl\
ationPyObject.lo\
ad_translation(m\
odel.abbrev)\x0a   \
             }\x0a \
           }\x0a   \
     }\x0a    }\x0a\x0a  \
  Action {\x0a     \
   text: qsTrans\
late(\x22MainWindow\
\x22, \x22&Appearance.\
..\x22)\x0a        onT\
riggered: {\x0a    \
        const co\
mponent = Qt.cre\
ateComponent(\x22qr\
c:/qml/component\
s/DialogAppearan\
ce.qml\x22)\x0a       \
     const dialo\
g = component.cr\
eateObject(appWi\
ndow)\x0a          \
  dialog.open()\x0a\
        }\x0a    }\x0a\
\x0a}\x0a\
\x00\x00\x03a\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Contr\
ols\x0a\x0a\x0aToolButton\
 {\x0a\x0a    icon.sou\
rce: \x22qrc:/data/\
icons/minimize_b\
lack_24dp.svg\x22\x0a \
   icon.width: 1\
8\x0a    icon.heigh\
t: 18\x0a\x0a    onCli\
cked: window.sho\
wMinimized()\x0a\x0a}\x0a\
\
\x00\x00\x07<\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Contr\
ols\x0a\x0a\x0aMenuAutoWi\
dth {\x0a\x0a    title\
: qsTranslate(\x22M\
ainWindow\x22, \x22&Vi\
deo\x22)\x0a\x0a    Actio\
n {\x0a        text\
: qsTranslate(\x22M\
ainWindow\x22, \x22Ope\
n &Video...\x22)\x0a  \
      shortcut: \
\x22CTRL+Shift+O\x22\x0a \
       onTrigger\
ed: {\x0a          \
  const componen\
t = Qt.createCom\
ponent(\x22qrc:/qml\
/components/Dial\
ogOpenVideo.qml\x22\
)\x0a            co\
nst dialog = com\
ponent.createObj\
ect(appWindow)\x0a \
           dialo\
g.open()\x0a       \
 }\x0a    }\x0a\x0a    Ac\
tion {\x0a        t\
ext: qsTranslate\
(\x22MainWindow\x22, \x22\
&Open Subtitles.\
..\x22)\x0a        onT\
riggered: {\x0a    \
        const co\
mponent = Qt.cre\
ateComponent(\x22qr\
c:/qml/component\
s/DialogOpenSubt\
itles.qml\x22)\x0a    \
        const di\
alog = component\
.createObject(ap\
pWindow)\x0a       \
     dialog.open\
()\x0a        }\x0a   \
 }\x0a\x0a    Action {\
\x0a        text: q\
sTranslate(\x22Main\
Window\x22, \x22Open &\
Network Stream..\
.\x22)\x0a        shor\
tcut: \x22CTRL+Alt+\
Shift+O\x22\x0a       \
 onTriggered: {\x0a\
            cons\
ole.log(\x22Open Ne\
twork Stream...\x22\
)\x0a        }\x0a    \
}\x0a\x0a    MenuSepar\
ator { }\x0a\x0a    Ac\
tion {\x0a        t\
ext: qsTranslate\
(\x22MainWindow\x22, \x22\
&Resize Video to\
 Original Resolu\
tion\x22)\x0a        s\
hortcut: \x22CTRL+R\
\x22\x0a        onTrig\
gered: {\x0a       \
     console.log\
(\x22Resize Video t\
o Original Resol\
ution\x22)\x0a        \
}\x0a    }\x0a\x0a}\x0a\
\x00\x00\x08O\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport QtQuic\
k.Layouts\x0aimport\
 models\x0aimport p\
yobjects\x0a\x0a\x0aDialo\
g {\x0a\x0a    width: \
420\x0a    height: \
540\x0a\x0a    modal: \
true\x0a    anchors\
.centerIn: paren\
t\x0a    standardBu\
ttons: Dialog.Ok\
\x0a    closePolicy\
: Popup.CloseOnE\
scape\x0a\x0a\x0a    cont\
entItem: ColumnL\
ayout {\x0a\x0a       \
 TabBar {\x0a      \
      id: bar\x0a  \
          conten\
tWidth: parent.w\
idth\x0a\x0a          \
  TabButton {\x0a  \
              te\
xt: qsTranslate(\
\x22AppearanceDialo\
g\x22, \x22Appearance\x22\
)\x0a            }\x0a\
        }\x0a\x0a     \
   StackLayout {\
\x0a\x0a            cu\
rrentIndex: bar.\
currentIndex\x0a   \
         Layout.\
leftMargin: 10\x0a \
           Layou\
t.topMargin: 20\x0a\
            Layo\
ut.rightMargin: \
10\x0a\x0a            \
ScrollView {\x0a\x0a  \
              Co\
lumnLayout {\x0a\x0a  \
                \
  width: parent.\
width\x0a\x0a         \
           Label\
DemiBold {\x0a     \
                \
   text: \x22Theme\x22\
\x0a\x0a              \
          Layout\
.topMargin: 8\x0a  \
                \
      Layout.bot\
tomMargin: 8\x0a   \
                \
     Layout.fill\
Width: true\x0a    \
                \
}\x0a\x0a             \
       DialogApp\
earanceViewTheme\
 {\x0a             \
           Layou\
t.fillWidth: tru\
e\x0a              \
      }\x0a\x0a       \
             Lab\
elDemiBold {\x0a   \
                \
     text: \x22Colo\
r\x22\x0a\x0a            \
            Layo\
ut.topMargin: 8\x0a\
                \
        Layout.b\
ottomMargin: 8\x0a \
                \
       Layout.fi\
llWidth: true\x0a  \
                \
  }\x0a\x0a           \
         DialogA\
ppearanceViewAcc\
ent {}\x0a\x0a        \
        }\x0a\x0a     \
       }\x0a\x0a      \
  }\x0a\x0a    }\x0a\x0a}\x0a\
\x00\x00\x00(\
m\
odule components\
\x0aPageMain PageMa\
in.qml\x0a\
\x00\x00\x0f\xdc\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport QtQuic\
k.Layouts\x0aimport\
 pyobjects\x0a\x0a\x0aCol\
umn {\x0a    id: ab\
outTab\x0a    spaci\
ng: 8\x0a    width:\
 parent.width\x0a  \
  topPadding: 15\
\x0a\x0a    Image {\x0a  \
      anchors.ho\
rizontalCenter: \
parent.horizonta\
lCenter\x0a        \
source: \x22qrc\x22 + \
DialogAboutPyObj\
ect.icon_resourc\
e\x0a        source\
Size.width: 150\x0a\
        sourceSi\
ze.height: 150\x0a \
       asynchron\
ous: true\x0a    }\x0a\
\x0a    Label {\x0a   \
     anchors.hor\
izontalCenter: p\
arent.horizontal\
Center\x0a        t\
ext: \x22mpvQC\x22\x0a   \
     font.bold: \
true\x0a        fon\
t.pixelSize: Qt.\
application.font\
.pixelSize * 1.2\
5\x0a    }\x0a\x0a    Row\
 {\x0a        ancho\
rs.horizontalCen\
ter: parent.hori\
zontalCenter\x0a   \
     spacing: 2\x0a\
\x0a        Label {\
\x0a            id:\
 version\x0a       \
     text: Dialo\
gAboutPyObject.t\
ag\x0a            f\
ont.bold: true\x0a \
       }\x0a\x0a      \
  Label {\x0a      \
      text: \x22-\x22\x0a\
            font\
.bold: true\x0a    \
        visible:\
 commitId.text !\
== \x22\x22\x0a        }\x0a\
\x0a        Label {\
\x0a            id:\
 commitId\x0a      \
      text: Dial\
ogAboutPyObject.\
commit_id\x0a      \
      font.bold:\
 true\x0a        }\x0a\
    }\x0a\x0a    Label\
 {\x0a        ancho\
rs.horizontalCen\
ter: parent.hori\
zontalCenter\x0a   \
     property ur\
l url: \x22https://\
github.com/mpvqc\
/mpvQC\x22\x0a\x0a       \
 text: \x22<html><s\
tyle type=\x5c'text\
/css\x5c'></style><\
a href=\x5c'\x22 + url\
 + \x22\x5c'>\x22 + url +\
 \x22</a></html>\x22\x0a \
       onLinkAct\
ivated: Qt.openU\
rlExternally(url\
)\x0a\x0a        Mouse\
Area {\x0a         \
   anchors.fill:\
 parent\x0a        \
    acceptedButt\
ons: Qt.NoButton\
 // we don't wan\
t to eat clicks \
on the Text\x0a    \
        cursorSh\
ape: parent.hove\
redLink ? Qt.Poi\
ntingHandCursor \
: Qt.ArrowCursor\
\x0a        }\x0a    }\
\x0a\x0a    Label {\x0a  \
      anchors.ho\
rizontalCenter: \
parent.horizonta\
lCenter\x0a\x0a       \
 text: \x22Copyrigh\
t \xc2\xa9 mpvQC Devel\
opers\x22\x0a        f\
ont.pixelSize: Q\
t.application.fo\
nt.pixelSize * 0\
.75\x0a    }\x0a\x0a    L\
abel {\x0a        w\
idth: parent.wid\
th\x0a        ancho\
rs.horizontalCen\
ter: parent.hori\
zontalCenter\x0a   \
     horizontalA\
lignment: Text.A\
lignHCenter\x0a    \
    wrapMode: Te\
xt.WordWrap\x0a\x0a   \
     property ur\
l licenceUrl: \x22h\
ttps://www.gnu.o\
rg/licenses/agpl\
-3.0.html\x22\x0a     \
   onLinkActivat\
ed: Qt.openUrlEx\
ternally(licence\
Url)\x0a\x0a        te\
xt: \x22<html><styl\
e type=\x5c'text/cs\
s\x5c'></style>\x0a   \
     This progra\
m comes with abs\
olutely no warra\
nty.\x0a        <br\
>\x0a        See th\
e\x0a        <a hre\
f=\x5c'\x22 + licenceU\
rl + \x22\x5c'>\x0a      \
      GNU Affero\
 General Public \
License, version\
 3 or later\x0a    \
    </a>\x0a       \
 for details.\x0a  \
      </html>\x22\x0a \
       font.pixe\
lSize: Qt.applic\
ation.font.pixel\
Size * 0.75\x0a\x0a   \
     MouseArea {\
\x0a            anc\
hors.fill: paren\
t\x0a            ac\
ceptedButtons: Q\
t.NoButton // we\
 don't want to e\
at clicks on the\
 Text\x0a          \
  cursorShape: p\
arent.hoveredLin\
k ? Qt.PointingH\
andCursor : Qt.A\
rrowCursor\x0a     \
   }\x0a    }\x0a\x0a    \
Rectangle { colo\
r: \x22transparent\x22\
; height: 15; wi\
dth: 10 }\x0a\x0a    R\
owLayout {\x0a     \
   width: parent\
.width\x0a\x0a        \
Label {\x0a        \
    Layout.prefe\
rredWidth: paren\
t.width / 2\x0a    \
        horizont\
alAlignment: Tex\
t.AlignRight\x0a   \
         text: \x22\
mpv version:\x22\x0a  \
      }\x0a\x0a       \
 Label {\x0a       \
     Layout.fill\
Width: true\x0a    \
        text: Di\
alogAboutPyObjec\
t.mpv_version\x0a  \
      }\x0a    }\x0a\x0a \
   RowLayout {\x0a \
       width: pa\
rent.width\x0a\x0a    \
    Label {\x0a    \
        Layout.p\
referredWidth: p\
arent.width / 2\x0a\
            hori\
zontalAlignment:\
 Text.AlignRight\
\x0a            tex\
t: \x22ffmpeg versi\
on:\x22\x0a        }\x0a\x0a\
        Label {\x0a\
            Layo\
ut.fillWidth: tr\
ue\x0a            t\
ext: DialogAbout\
PyObject.ffmpeg_\
version\x0a        \
}\x0a    }\x0a\x0a}\x0a\
\x00\x00\x05\xb7\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport pyobje\
cts\x0a\x0a\x0aListView {\
\x0a\x0a    id: listVi\
ew\x0a\x0a    clip: tr\
ue\x0a    reuseItem\
s: true\x0a    boun\
dsBehavior: Flic\
kable.StopAtBoun\
ds\x0a    model: Co\
mmentModelPyObje\
ct {}\x0a    Scroll\
Bar.vertical: Sc\
rollBar {}\x0a    d\
elegate: Compone\
nt {\x0a\x0a        id\
: contactsDelega\
te\x0a\x0a        Rect\
angle {\x0a\x0a       \
     width: list\
View.width\x0a     \
       height: c\
ontent.height\x0a  \
          color:\
 \x22transparent\x22\x0a/\
/            col\
or: ListView.isC\
urrentItem ? Mat\
erial.accent : \x22\
transparent\x22\x0a\x0a  \
          ListVi\
ewItem {\x0a\x0a      \
          id: co\
ntent\x0a\x0a         \
       index: mo\
del.index\x0a\x0a     \
           timeI\
nt: model.timeIn\
t\x0a              \
  timeStr: model\
.timeStr\x0a       \
         type: m\
odel.type\x0a      \
          commen\
t: model.comment\
\x0a\x0a            }\x0a\
\x0a        }\x0a\x0a    \
}\x0a\x0a}\x0a\x0a\
\x00\x00\x07\xb2\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport QtQuic\
k.Layouts\x0aimport\
 pyobjects\x0a\x0a\x0aIte\
m {\x0a\x0a    width: \
parent.width\x0a   \
 height: menuBar\
.height\x0a\x0a    Row\
Layout {\x0a       \
 width: parent.w\
idth\x0a        spa\
cing: 0\x0a\x0a       \
 MenuBar {\x0a     \
       id: menuB\
ar\x0a\x0a            \
MenuFile {}\x0a    \
        MenuVide\
o {}\x0a           \
 MenuOptions {}\x0a\
            Menu\
Help {}\x0a\x0a       \
     background:\
 Rectangle {\x0a   \
             col\
or: \x22transparent\
\x22\x0a            }\x0a\
\x0a        }\x0a\x0a    \
    Label {\x0a    \
        text: \x22m\
pvQC\x22\x0a          \
  horizontalAlig\
nment: Text.Alig\
nHCenter\x0a       \
     Layout.fill\
Width: true\x0a    \
    }\x0a\x0a        I\
tem {\x0a          \
  id: buttonWrap\
per\x0a            \
width: menuBar.w\
idth\x0a           \
 height: menuBar\
.height\x0a\x0a       \
     ButtonWindo\
wMinimize {\x0a    \
            heig\
ht: buttonWrappe\
r.height\x0a       \
         anchors\
.right: maximize\
Button.left\x0a    \
        }\x0a\x0a     \
       ButtonWin\
dowMaximize {\x0a  \
              id\
: maximizeButton\
\x0a               \
 height: buttonW\
rapper.height\x0a  \
              an\
chors.right: clo\
seButton.left\x0a  \
              ma\
ximized: window.\
visibility == Wi\
ndow.Maximized\x0a \
           }\x0a\x0a  \
          Button\
WindowClose {\x0a  \
              id\
: closeButton\x0a  \
              he\
ight: buttonWrap\
per.height\x0a     \
           ancho\
rs.right: button\
Wrapper.right\x0a  \
          }\x0a\x0a   \
     }\x0a\x0a    }\x0a\x0a}\
\x0a\
\x00\x00\x03\xb6\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Contr\
ols\x0a\x0a\x0aToolButton\
 {\x0a\x0a    id: butt\
on\x0a\x0a    property\
 int time\x0a\x0a    i\
con.source: \x22qrc\
:/data/icons/pla\
y_arrow_black_24\
dp.svg\x22\x0a    icon\
.width: 18\x0a    i\
con.height: 18\x0a\x0a\
    onClicked: {\
\x0a        console\
.log(\x22Play butto\
n clicked: \x22 + b\
utton.time)\x0a    \
}\x0a\x0a}\x0a\
\x00\x00\x03}\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Contr\
ols\x0a\x0a\x0aPage {\x0a\x0a  \
  header: Header\
Bar {}\x0a\x0a    foot\
er: TabBar {}\x0a\x0a \
   Page {\x0a\x0a     \
   anchors.fill:\
 parent\x0a\x0a       \
 PageMainSplitVi\
ew {\x0a\x0a          \
  anchors.fill: \
parent\x0a\x0a        \
}\x0a\x0a    }\x0a\x0a}\x0a\
\x00\x00\x08\xf1\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport QtQuic\
k.Layouts\x0aimport\
 pyobjects\x0a\x0a\x0aMpv\
PlayerPyObject {\
\x0a\x0a    id: mpv\x0a  \
  anchors.fill: \
parent\x0a\x0a    Mous\
eArea {\x0a        \
id: mouseArea\x0a\x0a \
       anchors.f\
ill: parent\x0a    \
    acceptedButt\
ons: Qt.LeftButt\
on | Qt.RightBut\
ton | Qt.MiddleB\
utton\x0a        ho\
verEnabled: true\
\x0a\x0a        onPosi\
tionChanged: eve\
nt => {\x0a        \
    mpv.move_mou\
se(event.x, even\
t.y)\x0a        }\x0a\x0a\
        onWheel:\
 event => {\x0a    \
        const de\
lta = event.angl\
eDelta\x0a         \
   if (delta.y =\
== 0 || delta.x \
!== 0) {\x0a       \
         return\x0a\
            }\x0a  \
          if (de\
lta.y > 0) {\x0a   \
             mpv\
.scroll_up()\x0a   \
         } else \
{\x0a              \
  mpv.scroll_dow\
n()\x0a            \
}\x0a        }\x0a\x0a   \
     onPressed: \
event => {\x0a     \
       const but\
ton = event.butt\
on\x0a            i\
f (button === Qt\
.LeftButton) {\x0a \
               m\
pv.press_mouse_l\
eft()\x0a          \
  } else if (but\
ton === Qt.Middl\
eButton) {\x0a     \
           mpv.p\
ress_mouse_middl\
e()\x0a            \
} else if (butto\
n === Qt.RightBu\
tton) {\x0a        \
        console.\
log(\x22todo: conte\
xt menu on right\
 button\x22)\x0a      \
      }\x0a        \
}\x0a\x0a        onRel\
eased: event => \
{\x0a            co\
nst button = eve\
nt.button\x0a      \
      if (button\
 === Qt.LeftButt\
on) {\x0a          \
      mpv.releas\
e_mouse_left()\x0a \
           }\x0a   \
     }\x0a\x0a        \
onDoubleClicked:\
 event => {\x0a    \
        const bu\
tton = event.but\
ton\x0a            \
if (button === Q\
t.LeftButton) {\x0a\
                \
console.log(\x22tod\
o: full screen o\
n double clicked\
 left button\x22)\x0a \
           }  el\
se if (button ==\
= Qt.MiddleButto\
n) {\x0a           \
     mpv.press_m\
ouse_middle()\x0a  \
          }\x0a    \
    }\x0a\x0a    }\x0a\x0a}\x0a\
\
\x00\x00\x05\x02\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Dialo\
gs\x0aimport pyobje\
cts\x0a\x0a\x0aFileDialog\
 {\x0a\x0a    title: q\
sTranslate(\x22File\
InteractionDialo\
gs\x22, \x22Open QC Do\
cument(s)\x22)\x0a    \
currentFolder: S\
ettingsPyObject.\
import_last_dir_\
documents\x0a    fi\
leMode: FileDial\
og.OpenFiles\x0a\x0a  \
  nameFilters: [\
\x0a        qsTrans\
late(\x22FileIntera\
ctionDialogs\x22, \x22\
QC documents\x22) +\
 \x22 (*.txt)\x22,\x0a   \
     qsTranslate\
(\x22FileInteractio\
nDialogs\x22, \x22All \
files\x22) + \x22 (*.*\
)\x22,\x0a    ]\x0a\x0a    o\
nAccepted: {\x0a   \
     SettingsPyO\
bject.import_las\
t_dir_documents \
= currentFolder.\
toString()\x0a     \
   for (let file\
 of selectedFile\
s) {\x0a           \
 console.log(\x22Op\
en: \x22 + file)\x0a  \
      }\x0a    }\x0a\x0a}\
\x0a\
\x00\x00\x03U\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0a\x0a\x0aLabel {\x0a\x0a  \
  font.weight: F\
ont.DemiBold\x0a   \
 font.pointSize:\
 14\x0a    font.bol\
d: true\x0a\x0a    hor\
izontalAlignment\
: Text.AlignLeft\
\x0a\x0a}\x0a\
\x00\x00\x05q\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Contr\
ols\x0a\x0a\x0aMenuAutoWi\
dth {\x0a\x0a    title\
: qsTranslate(\x22M\
ainWindow\x22, \x22&He\
lp\x22)\x0a\x0a    Action\
 {\x0a        text:\
 qsTranslate(\x22Ma\
inWindow\x22, \x22&Che\
ck for Updates..\
.\x22)\x0a        onTr\
iggered: {\x0a     \
       console.l\
og(\x22&Check for U\
pdates...\x22)\x0a    \
    }\x0a    }\x0a\x0a   \
 Action {\x0a      \
  text: qsTransl\
ate(\x22MainWindow\x22\
, \x22About &Qt\x22)\x0a \
       onTrigger\
ed: {\x0a          \
  console.log(\x22A\
bout Qt\x22)\x0a      \
  }\x0a    }\x0a\x0a    M\
enuSeparator { }\
\x0a\x0a    Action {\x0a \
       text: qsT\
ranslate(\x22MainWi\
ndow\x22, \x22About &m\
pvQC\x22)\x0a        o\
nTriggered: {\x0a  \
          const \
component = Qt.c\
reateComponent(\x22\
qrc:/qml/compone\
nts/DialogAbout.\
qml\x22)\x0a          \
  const dialog =\
 component.creat\
eObject(appWindo\
w)\x0a            d\
ialog.open()\x0a   \
     }\x0a    }\x0a\x0a}\x0a\
\
\x00\x00\x03;\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Contr\
ols\x0a\x0a\x0aToolButton\
 {\x0a\x0a    icon.sou\
rce: \x22qrc:/data/\
icons/more_vert_\
black_24dp.svg\x22\x0a\
    icon.width: \
18\x0a    icon.heig\
ht: 18\x0a\x0a}\x0a\
\x00\x00\x03\x97\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0a\x0a\x0aRectangle {\
\x0a\x0a    radius: wi\
dth * 0.5\x0a\x0a    s\
ignal clicked()\x0a\
\x0a    MouseArea {\
\x0a        anchors\
.fill: parent\x0a  \
      cursorShap\
e: Qt.PointingHa\
ndCursor\x0a       \
 onClicked: pare\
nt.clicked()\x0a   \
 }\x0a\x0a}\x0a\
\x00\x00\x05C\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0a\x0a\x0aMenu {\x0a\x0a   \
 /*\x0a    Taken an\
d adapted from:\x0a\
    https://mart\
in.rpdev.net/201\
8/03/13/qt-quick\
-controls-2-auto\
matically-set-th\
e-width-of-menus\
.html\x0a    */\x0a\x0a  \
  width: {\x0a     \
   let result = \
0\x0a        let pa\
dding = 0\x0a      \
  for (let i = 0\
; i < count; ++i\
) {\x0a            \
let item = itemA\
t(i)\x0a\x0a          \
  if (!isMenuSep\
arator(item)) {\x0a\
                \
result = Math.ma\
x(item.contentIt\
em.implicitWidth\
, result)\x0a      \
          paddin\
g = Math.max(ite\
m.padding, paddi\
ng)\x0a            \
}\x0a        }\x0a    \
    return resul\
t + padding * 2\x0a\
    }\x0a\x0a    funct\
ion isMenuSepara\
tor(item) {\x0a    \
    return item \
instanceof MenuS\
eparator\x0a    }\x0a\x0a\
}\x0a\
\x00\x00\x07\x19\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick\x0aimpor\
t QtQuick.Contro\
ls\x0aimport QtQuic\
k.Layouts\x0aimport\
 models\x0aimport p\
yobjects\x0a\x0a\x0aGridV\
iew {\x0a\x0a    id: g\
ridViewAccent\x0a\x0a \
   property int \
itemSize: 52\x0a   \
 property int it\
emPadding: 6\x0a   \
 property int it\
emBorder: 12\x0a\x0a  \
  model: AccentC\
olorModel {}\x0a   \
 focus: true\x0a   \
 clip: true\x0a    \
width: 352\x0a    h\
eight: (itemSize\
 + itemPadding) \
* 4\x0a    cellWidt\
h: itemSize + it\
emPadding\x0a    ce\
llHeight: itemSi\
ze + itemPadding\
\x0a\x0a    delegate: \
Component {\x0a\x0a   \
     Circle {\x0a\x0a \
           width\
: gridViewAccent\
.itemSize\x0a      \
      height: wi\
dth\x0a            \
color: appThemeC\
olorAccent === a\
ccentColor ? Mat\
erial.foreground\
 : \x22transparent\x22\
\x0a\x0a            Ci\
rcle {\x0a\x0a        \
        property\
 int colorFill: \
accentColor\x0a\x0a   \
             wid\
th: parent.width\
 - gridViewAccen\
t.itemBorder\x0a   \
             hei\
ght: width\x0a     \
           ancho\
rs.centerIn: par\
ent\x0a            \
    color:  Mate\
rial.accent\x0a\x0a   \
             Mat\
erial.accent: co\
lorFill\x0a\x0a       \
         onClick\
ed: {\x0a          \
          appWin\
dow.appThemeColo\
rAccent = colorF\
ill\x0a            \
        Settings\
PyObject.theme_a\
ccent = colorFil\
l\x0a              \
  }\x0a\x0a           \
 }\x0a\x0a        }\x0a\x0a \
   }\x0a\x0a}\x0a\
\x00\x00\x05b\
/\
*\x0ampvQC\x0a\x0aCopyrig\
ht (C) 2022 mpvQ\
C developers\x0a\x0aTh\
is program is fr\
ee software: you\
 can redistribut\
e it and/or modi\
fy\x0ait under the \
terms of the GNU\
 Affero General \
Public License a\
s published by\x0at\
he Free Software\
 Foundation, eit\
her version 3 of\
 the License, or\
\x0a(at your option\
) any later vers\
ion.\x0a\x0aThis progr\
am is distribute\
d in the hope th\
at it will be us\
eful,\x0abut WITHOU\
T ANY WARRANTY; \
without even the\
 implied warrant\
y of\x0aMERCHANTABI\
LITY or FITNESS \
FOR A PARTICULAR\
 PURPOSE.  See t\
he\x0aGNU Affero Ge\
neral Public Lic\
ense for more de\
tails.\x0a\x0aYou shou\
ld have received\
 a copy of the G\
NU Affero Genera\
l Public License\
\x0aalong with this\
 program.  If no\
t, see <http://w\
ww.gnu.org/licen\
ses/>.\x0a*/\x0a\x0a\x0aimpo\
rt QtQuick.Dialo\
gs\x0aimport pyobje\
cts\x0a\x0a\x0aFileDialog\
 {\x0a\x0a    title: q\
sTranslate(\x22File\
InteractionDialo\
gs\x22, \x22Open Subti\
tle(s)\x22)\x0a    cur\
rentFolder: Sett\
ingsPyObject.imp\
ort_last_dir_sub\
titles\x0a    fileM\
ode: FileDialog.\
OpenFiles\x0a\x0a    n\
ameFilters: [\x0a  \
      qsTranslat\
e(\x22FileInteracti\
onDialogs\x22, \x22Sub\
title files\x22) + \
\x22 (*.ass *.ssa *\
.srt *.sup *.idx\
 *.utf *.utf8 *.\
utf-8 *.smi *.rt\
 *.aqt *.jss *.j\
s *.mks *.vtt *.\
sub *.scc)\x22,\x0a   \
     qsTranslate\
(\x22FileInteractio\
nDialogs\x22, \x22All \
files\x22) + \x22 (*.*\
)\x22,\x0a    ]\x0a\x0a    o\
nAccepted: {\x0a   \
     SettingsPyO\
bject.import_las\
t_dir_subtitles \
= currentFolder.\
toString()\x0a     \
   for (let file\
 of selectedFile\
s) {\x0a           \
 console.log(\x22Op\
en: \x22 + file)\x0a  \
      }\x0a    }\x0a\x0a}\
\x0a\
\x00\x00\x005\
[\
Controls]\x0aStyle=\
Material\x0a\x0a[Mater\
ial]\x0aVariant=Den\
se\x0a\x0a\
\x00\x00\x0b\xd7\
<\
svg id=\x22Ebene_2\x22\
 data-name=\x22Eben\
e 2\x22 xmlns=\x22http\
://www.w3.org/20\
00/svg\x22 xmlns:xl\
ink=\x22http://www.\
w3.org/1999/xlin\
k\x22 viewBox=\x220 0 \
128 128\x22><defs><\
style>.cls-1{fil\
l:#6092c4;}.cls-\
2{fill:url(#Unbe\
nannter_Verlauf_\
171);}.cls-3{fil\
l:#fff;}.cls-4{f\
ill:#8ff0a4;}.cl\
s-5{fill:#e01b24\
;}.cls-6{opacity\
:0.34;}.cls-7{fi\
ll:none;stroke-w\
idth:4px;}.cls-7\
,.cls-8{stroke:#\
5e5e5e;stroke-mi\
terlimit:10;}.cl\
s-8{fill:#5e5e5e\
;}.cls-9{fill:#5\
f5c65;}.cls-10{f\
ill:url(#Unbenan\
nter_Verlauf_15)\
;}</style><linea\
rGradient id=\x22Un\
benannter_Verlau\
f_171\x22 x1=\x2264.15\
\x22 y1=\x22112.78\x22 x2\
=\x2264.15\x22 y2=\x224.3\
4\x22 gradientUnits\
=\x22userSpaceOnUse\
\x22><stop offset=\x22\
0\x22 stop-color=\x22#\
99c1f1\x22/><stop o\
ffset=\x221\x22 stop-c\
olor=\x22#aecdf0\x22/>\
</linearGradient\
><linearGradient\
 id=\x22Unbenannter\
_Verlauf_15\x22 x1=\
\x2273.52\x22 y1=\x2255.3\
6\x22 x2=\x2273.52\x22 y2\
=\x22116.72\x22 gradie\
ntUnits=\x22userSpa\
ceOnUse\x22><stop o\
ffset=\x220\x22 stop-c\
olor=\x22#9a9996\x22/>\
<stop offset=\x220.\
95\x22 stop-color=\x22\
#77767b\x22/></line\
arGradient></def\
s><path class=\x22c\
ls-1\x22 d=\x22M68.05,\
7.47A21.38,21.38\
,0,1,0,89.43,28.\
85,21.38,21.38,0\
,0,0,68.05,7.47Z\
m0,33.09A11.71,1\
1.71,0,1,1,79.76\
,28.85,11.71,11.\
71,0,0,1,68.05,4\
0.56Z\x22/><path cl\
ass=\x22cls-1\x22 d=\x22M\
34.07,18.5A15.22\
,15.22,0,1,0,49.\
28,33.72,15.21,1\
5.21,0,0,0,34.07\
,18.5Zm0,23.9a8.\
69,8.69,0,1,1,8.\
68-8.68A8.68,8.6\
8,0,0,1,34.07,42\
.4Z\x22/><path clas\
s=\x22cls-1\x22 d=\x22M11\
7.55,55.78v54.88\
c0,2.19-4.11,3.0\
8-5.94,1.28L80.3\
6,84.73a1.87,1.8\
7,0,0,1,0-3L111.\
61,54.5C113.44,5\
2.7,117.55,53.59\
,117.55,55.78Z\x22/\
><rect class=\x22cl\
s-1\x22 x=\x2210.75\x22 y\
=\x2249.86\x22 width=\x22\
84.79\x22 height=\x226\
6.76\x22 rx=\x228.54\x22/\
><path class=\x22cl\
s-2\x22 d=\x22M111.61,\
50.83l-16.06,14V\
54.56A8.54,8.54,\
0,0,0,87,46H74.7\
4A21.38,21.38,0,\
1,0,46.81,23.33,\
15.21,15.21,0,1,\
0,29.16,46H19.29\
a8.54,8.54,0,0,0\
-8.54,8.54v49.68\
a8.54,8.54,0,0,0\
,8.54,8.54H87a8.\
54,8.54,0,0,0,8.\
54-8.54v-10l16.0\
6,14c1.83,1.8,5.\
94.91,5.94-1.29V\
52.11C117.55,49.\
92,113.44,49,111\
.61,50.83ZM68.05\
,14A11.72,11.72,\
0,1,1,56.34,25.7\
2,11.71,11.71,0,\
0,1,68.05,14ZM25\
.39,31.63a8.68,8\
.68,0,1,1,8.68,8\
.68A8.68,8.68,0,\
0,1,25.39,31.63Z\
m23.48,3.49A21.4\
,21.4,0,0,0,61.3\
6,46H39A15.23,15\
.23,0,0,0,48.87,\
35.12Z\x22/><rect c\
lass=\x22cls-3\x22 x=\x22\
18.41\x22 y=\x2279.54\x22\
 width=\x2227.96\x22 h\
eight=\x223.41\x22/><r\
ect class=\x22cls-4\
\x22 x=\x2218.41\x22 y=\x228\
9.57\x22 width=\x2216.\
63\x22 height=\x223.76\
\x22/><rect class=\x22\
cls-3\x22 x=\x2238.59\x22\
 y=\x2289.57\x22 width\
=\x2211.12\x22 height=\
\x223.76\x22/><rect cl\
ass=\x22cls-3\x22 x=\x221\
8.41\x22 y=\x2299.78\x22 \
width=\x2231.99\x22 he\
ight=\x223.76\x22/><re\
ct class=\x22cls-5\x22\
 x=\x2257.23\x22 y=\x2284\
.74\x22 width=\x2217.4\
\x22 height=\x226.16\x22/\
><rect class=\x22cl\
s-3\x22 x=\x2247.1\x22 y=\
\x2274.55\x22 width=\x222\
2.8\x22 height=\x226.1\
6\x22/><g class=\x22cl\
s-6\x22><circle cla\
ss=\x22cls-7\x22 cx=\x226\
7.62\x22 cy=\x2285.11\x22\
 r=\x2221.82\x22/><rec\
t class=\x22cls-8\x22 \
x=\x2289.37\x22 y=\x2294.\
64\x22 width=\x226.17\x22\
 height=\x2230.56\x22 \
rx=\x223\x22 transform\
=\x22translate(-50.\
65 97.57) rotate\
(-45)\x22/></g><pat\
h class=\x22cls-9\x22 \
d=\x22M103.34,113.4\
7,87.19,97.32a24\
.82,24.82,0,1,0-\
4.36,4.37L99,117\
.83a3,3,0,0,0,4.\
2,0l.16-.15A3,3,\
0,0,0,103.34,113\
.47ZM48.78,82.14\
A18.84,18.84,0,1\
,1,67.62,101,18.\
87,18.87,0,0,1,4\
8.78,82.14Z\x22/><p\
ath class=\x22cls-1\
0\x22 d=\x22M103.34,11\
1.49,87.19,95.34\
a24.78,24.78,0,1\
,0-4.36,4.37L99,\
115.85a3,3,0,0,0\
,4.2,0l.16-.16A3\
,3,0,0,0,103.34,\
111.49ZM48.78,80\
.15A18.84,18.84,\
0,1,1,67.62,99,1\
8.86,18.86,0,0,1\
,48.78,80.15Z\x22/>\
</svg>\
\x00\x00\x00:\
[\
build_info]\x0atag=\
<inserted by CI>\
\x0acommit=<inserte\
d by CI>\x0a\
\x00\x00\x07\x16\
#\
################\
################\
###########\x0a# Th\
e following keys\
 are reserved by\
 mpvQC #\x0a# Chang\
ing them here wi\
ll have no effec\
t   #\x0a##########\
################\
################\
##\x0a\x0ae ignore\x0af i\
gnore\x0aUP ignore\x0a\
DOWN ignore\x0actrl\
+s ignore\x0actrl+S\
 ignore\x0actrl+n i\
gnore\x0actrl+o ign\
ore\x0actrl+q ignor\
e\x0actrl+O ignore\x0a\
ctrl+alt+O ignor\
e\x0actrl+r ignore\x0a\
MOUSE_BTN2 ignor\
e    # Right mou\
se click\x0a\x0a######\
################\
################\
############\x0a# T\
he following key\
s can be bound t\
o anything    #\x0a\
# This is not a \
comprehensive li\
st of all keys  \
 #\x0a# There are m\
any more, like a\
, A, @, \xc3\xb6, \xc3\xa9, \
\xc3\xae ... #\x0a# Pleas\
e never bind 'qu\
it' to any key! \
          #\x0a####\
################\
################\
##############\x0a\x0a\
SPACE cycle paus\
e\x0aLEFT no-osd se\
ek -2 relative+e\
xact\x0aRIGHT no-os\
d seek 2 relativ\
e+exact\x0ashift+LE\
FT osd-bar seek \
-5 relative+keyf\
rames\x0ashift+RIGH\
T osd-bar seek 5\
 relative+keyfra\
mes\x0actrl+LEFT no\
-osd sub-seek -1\
\x0actrl+RIGHT no-o\
sd sub-seek 1\x0a\x0aM\
OUSE_BTN0 cycle \
pause       # Le\
ft click on mous\
e\x0aMOUSE_BTN3 add\
 volume 2      #\
 Mouse wheel up\x0a\
MOUSE_BTN4 add v\
olume -2     # M\
ouse wheel down\x0a\
MOUSE_BTN5 add c\
hapter -1    # B\
ackward button o\
n mouse\x0aMOUSE_BT\
N6 add chapter 1\
     # Forward b\
utton on mouse\x0a\x0a\
p cycle pause\x0a. \
frame-step\x0a, fra\
me-back-step\x0a9 a\
dd volume -2\x0a0 a\
dd volume 2\x0am cy\
cle mute\x0aj cycle\
 sub\x0aJ cycle sub\
 down\x0aSHARP cycl\
e audio        #\
 SHARP assigns t\
he # key\x0al ab_lo\
op\x0as screenshot \
subtitles\x0aS scre\
enshot window\x0a\x0a#\
 This burns in s\
ubtitles (i.e. a\
lways render the\
m at video resol\
ution)\x0a# It cycl\
es through the v\
alues \x22no\x22 (Don'\
t blend subtitle\
s with the video\
)\x0a#             \
                \
 \x22yes\x22 (Blend at\
 display resolut\
ion)\x0a#          \
                \
    \x22video\x22 (Ble\
nd at video reso\
lution)\x0ab cycle \
blend-subtitles\x0a\
\x0a# This displays\
 statistics of t\
he currently pla\
yed file\x0ai scrip\
t-binding stats/\
display-stats-to\
ggle\x0a\
\x00\x00\x05\x1c\
#\
########\x0a# Video\
 #\x0a#########\x0a\x0a# \
HQ preset, uses \
Spline36 for ups\
caling and Mitch\
ell-Netravali fo\
r downscaling\x0apr\
ofile=gpu-hq\x0a\x0a# \
Debanding is dis\
abled because we\
 don't want to a\
lter the video w\
hile doing quali\
ty control\x0adeban\
d=no\x0a\x0a# Potentia\
lly higher quali\
ty video output.\
 Might be too de\
manding for old \
or low end hardw\
are\x0a#scale=ewa_l\
anczossharp\x0a#csc\
ale=ewa_lanczoss\
oft\x0a#dscale=lanc\
zos\x0a\x0a\x0a##########\
###\x0a# Subtitles \
#\x0a#############\x0a\
\x0a# This disables\
 the removal of \
very small gaps \
between subtitle\
 lines\x0a# This mi\
ght be a nice fe\
ature, but it hi\
des flaws in the\
 script\x0a# We don\
't want that whi\
le doing quality\
 control\x0asub-fix\
-timing=no\x0a\x0a# Th\
is makes sure th\
at the current s\
ubtitle line is \
loaded after see\
king\x0ademuxer-mkv\
-subtitle-prerol\
l=yes\x0a\x0a\x0a########\
###\x0a# OSC/OSD #\x0a\
###########\x0a\x0a# V\
ery slim On Scre\
en Controller th\
at consists of o\
nly a seekbar\x0a# \
Change the value\
 of osc-valign t\
o set the vertic\
al position (Val\
ues between -1 a\
nd 1 are allowed\
)\x0ascript-opts=os\
c-minmousemove=0\
,osc-hidetimeout\
=200,osc-layout=\
slimbox,osc-vali\
gn=0.6\x0aosd-bar-a\
lign-y=0\x0a\x0a# Bigg\
er On Screen Con\
troller with man\
y buttons\x0a#scrip\
t-opts=osc-minmo\
usemove=0,osc-hi\
detimeout=200,os\
c-layout=box,osc\
-valign=0.5\x0a\x0a\x0a##\
#############\x0a# \
Screenshots #\x0a##\
#############\x0a\x0a#\
screenshot-direc\
tory=\x0ascreenshot\
-format=png\x0ascre\
enshot-high-bit-\
depth=no\x0a\x0a\x0a\
\x00\x00\x00\xaf\
<\
svg xmlns=\x22http:\
//www.w3.org/200\
0/svg\x22 height=\x222\
4px\x22 viewBox=\x220 \
0 24 24\x22 width=\x22\
24px\x22 fill=\x22#000\
000\x22><path d=\x22M0\
 0h24v24H0V0z\x22 f\
ill=\x22none\x22/><pat\
h d=\x22M6 19h12v2H\
6v-2z\x22/></svg>\
\x00\x00\x01\x17\
<\
svg xmlns=\x22http:\
//www.w3.org/200\
0/svg\x22 enable-ba\
ckground=\x22new 0 \
0 24 24\x22 height=\
\x2224px\x22 viewBox=\x22\
0 0 24 24\x22 width\
=\x2224px\x22 fill=\x22#0\
00000\x22><rect fil\
l=\x22none\x22 height=\
\x2224\x22 width=\x2224\x22/\
><polygon points\
=\x2221,11 21,3 13,\
3 16.29,6.29 6.2\
9,16.29 3,13 3,2\
1 11,21 7.71,17.\
71 17.71,7.71\x22/>\
</svg>\
\x00\x00\x016\
<\
svg xmlns=\x22http:\
//www.w3.org/200\
0/svg\x22 enable-ba\
ckground=\x22new 0 \
0 24 24\x22 height=\
\x2224px\x22 viewBox=\x22\
0 0 24 24\x22 width\
=\x2224px\x22 fill=\x22#0\
00000\x22><rect fil\
l=\x22none\x22 height=\
\x2224\x22 width=\x2224\x22/\
><path d=\x22M22,3.\
41l-5.29,5.29L20\
,12h-8V4l3.29,3.\
29L20.59,2L22,3.\
41z M3.41,22l5.2\
9-5.29L12,20v-8H\
4l3.29,3.29L2,20\
.59L3.41,22z\x22/><\
/svg>\
\x00\x00\x010\
<\
svg xmlns=\x22http:\
//www.w3.org/200\
0/svg\x22 height=\x222\
4px\x22 viewBox=\x220 \
0 24 24\x22 width=\x22\
24px\x22 fill=\x22#000\
000\x22><path d=\x22M0\
 0h24v24H0V0z\x22 f\
ill=\x22none\x22/><pat\
h d=\x22M12 8c1.1 0\
 2-.9 2-2s-.9-2-\
2-2-2 .9-2 2 .9 \
2 2 2zm0 2c-1.1 \
0-2 .9-2 2s.9 2 \
2 2 2-.9 2-2-.9-\
2-2-2zm0 6c-1.1 \
0-2 .9-2 2s.9 2 \
2 2 2-.9 2-2-.9-\
2-2-2z\x22/></svg>\
\x00\x00\x01\x0c\
<\
svg xmlns=\x22http:\
//www.w3.org/200\
0/svg\x22 height=\x222\
4px\x22 viewBox=\x220 \
0 24 24\x22 width=\x22\
24px\x22 fill=\x22#000\
000\x22><path d=\x22M0\
 0h24v24H0V0z\x22 f\
ill=\x22none\x22/><pat\
h d=\x22M19 6.41L17\
.59 5 12 10.59 6\
.41 5 5 6.41 10.\
59 12 5 17.59 6.\
41 19 12 13.41 1\
7.59 19 19 17.59\
 13.41 12 19 6.4\
1z\x22/></svg>\
\x00\x00\x00\xdf\
<\
svg xmlns=\x22http:\
//www.w3.org/200\
0/svg\x22 height=\x222\
4px\x22 viewBox=\x220 \
0 24 24\x22 width=\x22\
24px\x22 fill=\x22#000\
000\x22><path d=\x22M8\
 6.82v10.36c0 .7\
9.87 1.27 1.54.8\
4l8.14-5.18c.62-\
.39.62-1.29 0-1.\
69L9.54 5.98C8.8\
7 5.55 8 6.03 8 \
6.82z\x22/></svg>\
"

qt_resource_name = b"\
\x00\x04\
\x00\x06\xa8\xa1\
\x00d\
\x00a\x00t\x00a\
\x00\x03\
\x00\x00x<\
\x00q\
\x00m\x00l\
\x00\x02\
\x00\x00\x07}\
\x00q\
\x00m\
\x00\x05\
\x00j\x85}\
\x00d\
\x00e\x00.\x00q\x00m\
\x00\x0a\
\x07j\x093\
\x00c\
\x00o\x00m\x00p\x00o\x00n\x00e\x00n\x00t\x00s\
\x00\x07\
\x0e\xc3lS\
\x00h\
\x00e\x00l\x00p\x00e\x00r\x00s\
\x00\x14\
\x05\xd2\x1cS\
\x00w\
\x00i\x00n\x00d\x00o\x00w\x00-\x00o\x00p\x00e\x00r\x00a\x00t\x00i\x00o\x00n\x00s\
\x00.\x00j\x00s\
\x00\x06\
\x07E\xac3\
\x00m\
\x00o\x00d\x00e\x00l\x00s\
\x00\x08\
\x08K!S\
\x00h\
\x00a\x00n\x00d\x00l\x00e\x00r\x00s\
\x00\x08\
\x08\x01Z\x5c\
\x00m\
\x00a\x00i\x00n\x00.\x00q\x00m\x00l\
\x00\x06\
\x07\x84+\x02\
\x00q\
\x00m\x00l\x00d\x00i\x00r\
\x00\x1b\
\x07\xf7\xe7\xbc\
\x00W\
\x00i\x00n\x00d\x00o\x00w\x00B\x00o\x00r\x00d\x00e\x00r\x00M\x00o\x00u\x00s\x00e\
\x00C\x00u\x00r\x00s\x00e\x00r\x00.\x00q\x00m\x00l\
\x00\x17\
\x0a5T\xbc\
\x00W\
\x00i\x00n\x00d\x00o\x00w\x00R\x00e\x00s\x00i\x00z\x00e\x00H\x00a\x00n\x00d\x00l\
\x00e\x00r\x00.\x00q\x00m\x00l\
\x00\x14\
\x08\xa2\xfe\xfc\
\x00A\
\x00c\x00c\x00e\x00n\x00t\x00C\x00o\x00l\x00o\x00r\x00M\x00o\x00d\x00e\x00l\x00.\
\x00q\x00m\x00l\
\x00\x12\
\x04\xd4\x90|\
\x00D\
\x00e\x00v\x00e\x00l\x00o\x00p\x00e\x00r\x00M\x00o\x00d\x00e\x00l\x00.\x00q\x00m\
\x00l\
\x00\x11\
\x0d\x0e\x0f<\
\x00L\
\x00a\x00n\x00g\x00u\x00a\x00g\x00e\x00M\x00o\x00d\x00e\x00l\x00.\x00q\x00m\x00l\
\
\x00\x10\
\x06{r|\
\x00A\
\x00r\x00t\x00w\x00o\x00r\x00k\x00M\x00o\x00d\x00e\x00l\x00.\x00q\x00m\x00l\
\x00\x13\
\x091\x91\x9c\
\x00D\
\x00e\x00p\x00e\x00n\x00d\x00e\x00n\x00c\x00y\x00M\x00o\x00d\x00e\x00l\x00.\x00q\
\x00m\x00l\
\x00\x0e\
\x078\x02<\
\x00T\
\x00h\x00e\x00m\x00e\x00M\x00o\x00d\x00e\x00l\x00.\x00q\x00m\x00l\
\x00\x1e\
\x0a\xe5q<\
\x00C\
\x00o\x00m\x00m\x00e\x00n\x00t\x00T\x00y\x00p\x00e\x00W\x00i\x00d\x00t\x00h\x00C\
\x00a\x00l\x00c\x00u\x00l\x00a\x00t\x00o\x00r\x00.\x00q\x00m\x00l\
\x00\x0c\
\x06`\xe7\xbc\
\x00M\
\x00e\x00n\x00u\x00F\x00i\x00l\x00e\x00.\x00q\x00m\x00l\
\x00\x13\
\x0d\xba\xfc\x9c\
\x00D\
\x00i\x00a\x00l\x00o\x00g\x00O\x00p\x00e\x00n\x00V\x00i\x00d\x00e\x00o\x00.\x00q\
\x00m\x00l\
\x00\x18\
\x02\xd5{\xbc\
\x00B\
\x00u\x00t\x00t\x00o\x00n\x00W\x00i\x00n\x00d\x00o\x00w\x00M\x00a\x00x\x00i\x00m\
\x00i\x00z\x00e\x00.\x00q\x00m\x00l\
\x00\x0d\
\x05\xea\x11\xdc\
\x00H\
\x00e\x00a\x00d\x00e\x00r\x00B\x00a\x00r\x00.\x00q\x00m\x00l\
\x00\x10\
\x04_\x0a|\
\x00L\
\x00a\x00b\x00e\x00l\x00C\x00o\x00m\x00m\x00e\x00n\x00t\x00.\x00q\x00m\x00l\
\x00\x15\
\x01#\x9a\x1c\
\x00B\
\x00u\x00t\x00t\x00o\x00n\x00W\x00i\x00n\x00d\x00o\x00w\x00C\x00l\x00o\x00s\x00e\
\x00.\x00q\x00m\x00l\
\x00\x0d\
\x04\x99\xd6|\
\x00L\
\x00a\x00b\x00e\x00l\x00T\x00y\x00p\x00e\x00.\x00q\x00m\x00l\
\x00\x0d\
\x0c\xc9\xd6<\
\x00L\
\x00a\x00b\x00e\x00l\x00T\x00i\x00m\x00e\x00.\x00q\x00m\x00l\
\x00\x10\
\x097\x0e\x9c\
\x00L\
\x00i\x00s\x00t\x00V\x00i\x00e\x00w\x00I\x00t\x00e\x00m\x00.\x00q\x00m\x00l\
\x00\x15\
\x0d\xa3\x18\xbc\
\x00P\
\x00a\x00g\x00e\x00M\x00a\x00i\x00n\x00S\x00p\x00l\x00i\x00t\x00V\x00i\x00e\x00w\
\x00.\x00q\x00m\x00l\
\x00\x1a\
\x00k\xa5\x9c\
\x00D\
\x00i\x00a\x00l\x00o\x00g\x00A\x00b\x00o\x00u\x00t\x00V\x00i\x00e\x00w\x00C\x00r\
\x00e\x00d\x00i\x00t\x00s\x00.\x00q\x00m\x00l\
\x00\x0f\
\x06\xad\x14\xfc\
\x00D\
\x00i\x00a\x00l\x00o\x00g\x00A\x00b\x00o\x00u\x00t\x00.\x00q\x00m\x00l\
\x00\x1d\
\x0a\xb4\xd5\xdc\
\x00D\
\x00i\x00a\x00l\x00o\x00g\x00A\x00p\x00p\x00e\x00a\x00r\x00a\x00n\x00c\x00e\x00V\
\x00i\x00e\x00w\x00T\x00h\x00e\x00m\x00e\x00.\x00q\x00m\x00l\
\x00\x0f\
\x01\x1b\xef\x1c\
\x00M\
\x00e\x00n\x00u\x00O\x00p\x00t\x00i\x00o\x00n\x00s\x00.\x00q\x00m\x00l\
\x00\x18\
\x02\xdc;\xbc\
\x00B\
\x00u\x00t\x00t\x00o\x00n\x00W\x00i\x00n\x00d\x00o\x00w\x00M\x00i\x00n\x00i\x00m\
\x00i\x00z\x00e\x00.\x00q\x00m\x00l\
\x00\x0d\
\x0dM\x10\x9c\
\x00M\
\x00e\x00n\x00u\x00V\x00i\x00d\x00e\x00o\x00.\x00q\x00m\x00l\
\x00\x14\
\x04N\x0f\xdc\
\x00D\
\x00i\x00a\x00l\x00o\x00g\x00A\x00p\x00p\x00e\x00a\x00r\x00a\x00n\x00c\x00e\x00.\
\x00q\x00m\x00l\
\x00\x18\
\x07\xa7\x93\xfc\
\x00D\
\x00i\x00a\x00l\x00o\x00g\x00A\x00b\x00o\x00u\x00t\x00V\x00i\x00e\x00w\x00A\x00b\
\x00o\x00u\x00t\x00.\x00q\x00m\x00l\
\x00\x14\
\x00I\xc6\x1c\
\x00L\
\x00i\x00s\x00t\x00V\x00i\x00e\x00w\x00C\x00o\x00m\x00m\x00e\x00n\x00t\x00s\x00.\
\x00q\x00m\x00l\
\x00\x14\
\x09h\xa2\x1c\
\x00H\
\x00e\x00a\x00d\x00e\x00r\x00B\x00a\x00r\x00C\x00o\x00n\x00t\x00e\x00n\x00t\x00.\
\x00q\x00m\x00l\
\x00\x0e\
\x0b\xfe\x84\xbc\
\x00B\
\x00u\x00t\x00t\x00o\x00n\x00P\x00l\x00a\x00y\x00.\x00q\x00m\x00l\
\x00\x0c\
\x0dN\xe4\x5c\
\x00P\
\x00a\x00g\x00e\x00M\x00a\x00i\x00n\x00.\x00q\x00m\x00l\
\x00\x0a\
\x0f\xcf\xb5<\
\x00P\
\x00l\x00a\x00y\x00e\x00r\x00.\x00q\x00m\x00l\
\x00\x17\
\x06Q\x22\xbc\
\x00D\
\x00i\x00a\x00l\x00o\x00g\x00O\x00p\x00e\x00n\x00D\x00o\x00c\x00u\x00m\x00e\x00n\
\x00t\x00s\x00.\x00q\x00m\x00l\
\x00\x11\
\x06\x06\xd0\x1c\
\x00L\
\x00a\x00b\x00e\x00l\x00D\x00e\x00m\x00i\x00B\x00o\x00l\x00d\x00.\x00q\x00m\x00l\
\
\x00\x0c\
\x02K\xe7\xfc\
\x00M\
\x00e\x00n\x00u\x00H\x00e\x00l\x00p\x00.\x00q\x00m\x00l\
\x00\x0e\
\x0f\xf2\x84\x5c\
\x00B\
\x00u\x00t\x00t\x00o\x00n\x00M\x00o\x00r\x00e\x00.\x00q\x00m\x00l\
\x00\x0a\
\x0a1\x19<\
\x00C\
\x00i\x00r\x00c\x00l\x00e\x00.\x00q\x00m\x00l\
\x00\x11\
\x0br\xdd\xbc\
\x00M\
\x00e\x00n\x00u\x00A\x00u\x00t\x00o\x00W\x00i\x00d\x00t\x00h\x00.\x00q\x00m\x00l\
\
\x00\x1e\
\x04\x10\xa9\x5c\
\x00D\
\x00i\x00a\x00l\x00o\x00g\x00A\x00p\x00p\x00e\x00a\x00r\x00a\x00n\x00c\x00e\x00V\
\x00i\x00e\x00w\x00A\x00c\x00c\x00e\x00n\x00t\x00.\x00q\x00m\x00l\
\x00\x17\
\x02\xfbH\x1c\
\x00D\
\x00i\x00a\x00l\x00o\x00g\x00O\x00p\x00e\x00n\x00S\x00u\x00b\x00t\x00i\x00t\x00l\
\x00e\x00s\x00.\x00q\x00m\x00l\
\x00\x05\
\x00o\xa6S\
\x00i\
\x00c\x00o\x00n\x00s\
\x00\x15\
\x08\x1e\x16f\
\x00q\
\x00t\x00q\x00u\x00i\x00c\x00k\x00c\x00o\x00n\x00t\x00r\x00o\x00l\x00s\x002\x00.\
\x00c\x00o\x00n\x00f\
\x00\x08\
\x0aaW'\
\x00i\
\x00c\x00o\x00n\x00.\x00s\x00v\x00g\
\x00\x06\
\x06\xa6L\xf7\
\x00c\
\x00o\x00n\x00f\x00i\x00g\
\x00\x0f\
\x0dk}\xc6\
\x00b\
\x00u\x00i\x00l\x00d\x00-\x00i\x00n\x00f\x00o\x00.\x00c\x00o\x00n\x00f\
\x00\x0a\
\x0cz\xb0\xa6\
\x00i\
\x00n\x00p\x00u\x00t\x00.\x00c\x00o\x00n\x00f\
\x00\x08\
\x07\x94\xac\xc6\
\x00m\
\x00p\x00v\x00.\x00c\x00o\x00n\x00f\
\x00\x17\
\x0d\xa5\x80\x07\
\x00m\
\x00i\x00n\x00i\x00m\x00i\x00z\x00e\x00_\x00b\x00l\x00a\x00c\x00k\x00_\x002\x004\
\x00d\x00p\x00.\x00s\x00v\x00g\
\x00\x1b\
\x0bil\x07\
\x00o\
\x00p\x00e\x00n\x00_\x00i\x00n\x00_\x00f\x00u\x00l\x00l\x00_\x00b\x00l\x00a\x00c\
\x00k\x00_\x002\x004\x00d\x00p\x00.\x00s\x00v\x00g\
\x00\x1f\
\x03\xe6\x1d\xe7\
\x00c\
\x00l\x00o\x00s\x00e\x00_\x00f\x00u\x00l\x00l\x00s\x00c\x00r\x00e\x00e\x00n\x00_\
\x00b\x00l\x00a\x00c\x00k\x00_\x002\x004\x00d\x00p\x00.\x00s\x00v\x00g\
\x00\x18\
\x07U\xb3'\
\x00m\
\x00o\x00r\x00e\x00_\x00v\x00e\x00r\x00t\x00_\x00b\x00l\x00a\x00c\x00k\x00_\x002\
\x004\x00d\x00p\x00.\x00s\x00v\x00g\
\x00\x14\
\x03\xe9\x9d'\
\x00c\
\x00l\x00o\x00s\x00e\x00_\x00b\x00l\x00a\x00c\x00k\x00_\x002\x004\x00d\x00p\x00.\
\x00s\x00v\x00g\
\x00\x19\
\x01C\x83\x07\
\x00p\
\x00l\x00a\x00y\x00_\x00a\x00r\x00r\x00o\x00w\x00_\x00b\x00l\x00a\x00c\x00k\x00_\
\x002\x004\x00d\x00p\x00.\x00s\x00v\x00g\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x1a\x00\x02\x00\x00\x00\x01\x00\x00\x00C\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x0e\x00\x02\x00\x00\x00\x06\x00\x00\x00\x11\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x05\x00\x00\x00\x04\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x07\x98\x00\x02\x00\x00\x00\x06\x00\x00\x00\x0b\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x07\xee\x00\x02\x00\x00\x00\x02\x00\x00\x00\x09\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x07\xa8\x00\x00\x00\x00\x00\x01\x00\x00\xe6\xb2\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x07\xd8\x00\x00\x00\x00\x00\x01\x00\x00\xe6\xeb\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x08\x00\x00\x00\x00\x00\x00\x01\x00\x00\xf2\xc6\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x08>\x00\x00\x00\x00\x00\x01\x00\x00\xfa\x1e\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x08$\x00\x00\x00\x00\x00\x01\x00\x00\xf3\x04\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x09l\x00\x00\x00\x00\x00\x01\x00\x01\x04\x8a\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x08\xc4\x00\x00\x00\x00\x00\x01\x00\x01\x01\x0c\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x09>\x00\x00\x00\x00\x00\x01\x00\x01\x03z\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x09\x08\x00\x00\x00\x00\x00\x01\x00\x01\x02F\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x08\x88\x00\x00\x00\x00\x00\x01\x00\x00\xff\xf1\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x08T\x00\x00\x00\x00\x00\x01\x00\x00\xff>\
\x00\x00\x01\x80\x13u\xd6_\
\x00\x00\x00b\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa5\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x00\x90\x00\x02\x00\x00\x00\x07\x00\x00\x00<\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x004\x00\x02\x00\x00\x00 \x00\x00\x00\x1c\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\xb8\x00\x00\x00\x00\x00\x01\x00\x00\x03\xfe\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x00\xa2\x00\x02\x00\x00\x00\x03\x00\x00\x00\x19\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00N\x00\x02\x00\x00\x00\x02\x00\x00\x00\x17\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\xce\x00\x00\x00\x00\x00\x01\x00\x002\xa6\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x02D\x00\x00\x00\x00\x00\x01\x00\x002\xfd\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x00\xce\x00\x00\x00\x00\x00\x01\x00\x00\x0a\x99\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x00\xe0\x00\x00\x00\x00\x00\x01\x00\x00\x0b\x0d\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x01\x1c\x00\x00\x00\x00\x00\x01\x00\x00\x10s\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x05\x8e\x00\x00\x00\x00\x00\x01\x00\x00\xa2\x99\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x04\x12\x00\x01\x00\x00\x00\x01\x00\x00h\x89\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x04\xb0\x00\x00\x00\x00\x00\x01\x00\x00xm\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x03L\x00\x00\x00\x00\x00\x01\x00\x00Q\xe3\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x06\xa0\x00\x00\x00\x00\x00\x01\x00\x00\xc8\x99\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x02\xd0\x00\x00\x00\x00\x00\x01\x00\x00E\x92\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x04\xd4\x00\x00\x00\x00\x00\x01\x00\x00\x7f\x95\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x07d\x00\x00\x00\x00\x00\x01\x00\x00\xe1L\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x07\x22\x00\x00\x00\x00\x00\x01\x00\x00\xda/\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x05*\x00\x00\x00\x00\x00\x01\x00\x00\x8a:\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x03&\x00\x00\x00\x00\x00\x01\x00\x00N3\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x03|\x00\x00\x00\x00\x00\x01\x00\x00U=\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x03\x06\x00\x00\x00\x00\x00\x01\x00\x00I\xc0\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x06x\x00\x00\x00\x00\x00\x01\x00\x00\xc5@\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x06D\x00\x00\x00\x00\x00\x01\x00\x00\xc0:\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x02\x86\x00\x00\x00\x00\x00\x01\x00\x009p\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x04L\x00\x00\x00\x00\x00\x01\x00\x00l\x92\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x00\xce\x00\x00\x00\x00\x00\x01\x00\x00\x92\x8d\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x05X\x00\x00\x00\x00\x00\x01\x00\x00\x92\xb9\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x03\xbc\x00\x00\x00\x00\x00\x01\x00\x00\x5c6\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x05\xbc\x00\x00\x00\x00\x00\x01\x00\x00\xa8T\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x06\xe0\x00\x00\x00\x00\x00\x01\x00\x00\xd1M\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x04p\x00\x00\x00\x00\x00\x01\x00\x00r(\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x06\xfa\x00\x00\x00\x00\x00\x01\x00\x00\xd4\xe8\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x05\xea\x00\x00\x00\x00\x00\x01\x00\x00\xb0\x0a\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x03\x9c\x00\x00\x00\x00\x00\x01\x00\x00X\xe7\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x05\x0a\x00\x00\x00\x00\x00\x01\x00\x00\x82\xfa\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x06\x0c\x00\x00\x00\x00\x00\x01\x00\x00\xb3\xc4\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x03\xe2\x00\x00\x00\x00\x00\x01\x00\x00c@\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x02\xa4\x00\x00\x00\x00\x00\x01\x00\x00@\xc6\
\x00\x00\x01\x80\x13u\xd6^\
\x00\x00\x06*\x00\x00\x00\x00\x00\x01\x00\x00\xb7E\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x06\xbe\x00\x00\x00\x00\x00\x01\x00\x00\xce\x0e\
\x00\x00\x01\x80\x13u\xd6]\
\x00\x00\x01~\x00\x00\x00\x00\x00\x01\x00\x00\x1d\x90\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x01\xd0\x00\x00\x00\x00\x00\x01\x00\x00&\x8a\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x02\x22\x00\x00\x00\x00\x00\x01\x00\x00/b\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x00\xce\x00\x00\x00\x00\x00\x01\x00\x00\x15i\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x01P\x00\x00\x00\x00\x00\x01\x00\x00\x16?\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x01\xf6\x00\x00\x00\x00\x00\x01\x00\x00)\x8b\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x01\xa8\x00\x00\x00\x00\x00\x01\x00\x00 \xc0\
\x00\x00\x01\x80\x13u\xd6\x5c\
\x00\x00\x00$\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x80\x13u\xd6_\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
