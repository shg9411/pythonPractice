import math
import os
from django.shortcuts import redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from board.models import Board, Comment
from django.utils.http import urlquote

#파일이 업로드 될 디렉토리 지정
UPLOAD_DIR = "d:/upload/"

def list(request):
    #레코드 갯수
    boardCount = Board.objects.count()
    #글번호 내림차순
    boardList = Board.objects.all().order_by("-idx")
    #포워딩
    return render_to_response("list.html",{"boardList":boardList, "boardCount":boardCount})

def write(request):
    return render_to_response("write.html")

@csrf_exempt
def insert(request):
    print(request)
    #파일 업로드 작업
    fname = ""
    fsize = 0
    #업로드된 파일이 있으면
    if "file" in request.FILES:
        file = request.FILES["file"]
        fname = file._name
        fp = open("%s%s" % (UPLOAD_DIR,fname),"wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
        fsize=os.path.getsize(UPLOAD_DIR+fname)
    dto = Board(writer=request.POST["writer"],
                title=request.POST["title"],
                content=request.POST["content"],
                filename=fname,
                filesize=fsize)
    #insert 실행
    dto.save()
    #콘솔에 출력
    print(dto)
    #목록으로 이동
    return redirect("/")

def download(request):
    id = request.GET["idx"]
    dto = Board.objects.get(idx = id)
    path = UPLOAD_DIR+dto.filename
    print("path:",path)
    # 디렉토리 이름 빼고
    filename=os.path.basename(path)
    #특수문자 빼고
    filename=urlquote(filename)
    print("pfilename:",os.path.basename(path))
    with open(path,'rb') as file:
        #파일 종류가 다양하므로 octet-stream으로 선언
        response = HttpResponse(file.read(), content_type="application/octet-stream")
        #첨부파일의 이름(한글 파일 이름이 깨지지 않도록 처리
        response["Content-Disposition"] = \
            "attachment; filename*=UTF-8''{0}".format(filename)
        #다운횟수증가
        dto.down_up()
        dto.save()
        return response

def detail(request):
    id = request.GET["idx"]
    dto = Board.objects.get(idx = id)
    dto.hit_up()
    dto.save()
    filesize = "%.2f" % (dto.filesize / 1024)
    commentList=Comment.objects.filter(board_idx=id).order_by("idx")
    return render_to_response("detail.html",{"dto":dto,"filesize":filesize,"commentList":commentList})

@csrf_exempt
def reply_insert(request):
    id = request.POST["idx"]
    dto = Comment(board_idx=id, writer=request.POST["writer"],
                  content=request.POST["content"])
    dto.save()
    return HttpResponseRedirect("detail?idx="+id)

@csrf_exempt
def update(request):
    id = request.POST['idx']
    dto_src = Board.objects.get(idx=id)
    fname=dto_src.filename
    fsize=dto_src.filesize
    if "file" in request.FILES:
        file = request.FILES["file"]
        fname = file._name
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
        fsize=os.path.getsize(UPLOAD_DIR+fname)
    dto_new = Board(idx = id, writer=request.POST["writer"],
                    title=request.POST["title"],
                    content=request.POST["content"],
                    filename=fname, filesize=fsize)
    dto_new.save()
    return redirect("/")

@csrf_exempt
def delete(request):
    id = request.POST["idx"]
    Board.objects.get(idx=id).delete()
    return redirect("/")