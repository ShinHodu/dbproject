/* Templates: 기본 html을 만들어 놓고 일부만 수정해서 사용
앱구조 디렉토리: templates아래에 여러 html파일을 만들어 놓고 부른다
/application.py
/templates
    /hello.html

함수: render_templates(html파일이름, keyword=변수들...)
여러 변수들 저장->html파일의 값들 수정-> 새로운 html파일 생성
*/

from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html',name=name)

/* html: <hello.html>
<!doctype html>
<title> Hello from Flask </title>
{%if name%}
    <h1> Hello {{name}}! </h1>
{%else%} 
    <h1> Hello, World! </h1>
{%end if%}

*/
//전달받은 함수 name이 None이 아니라면 Hello name반환
//ex)name=Eunna면 Hello Eunna반환
//아니면 Hello, World! 반환

/* 변환된 html: <Generated hello.html>
<title> Hello from Flask</title>
<h1> Hello Eunna </h1>
*/