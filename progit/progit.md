## Pro git

Pro git(2판)을 읽으면서 잘 모르겠거나 도움이 될 것 같은 명령어 및 git 사용 팁들을 기록

**staged 상태 파일의 변화 확인하기**
`git diff --cached`

**Staging 생략하기**
`git commit -a`

**파일. 삭제하기: git rm 명령으로 tracked 상태 파일을 삭제한 뒤 커밋해야함**
`git rm test.txt`
`git rm --cached README`: 워킹 디렉토리에 파일은 그대로 남겨놓기 (gitignore 파일을 실수로 올리는 등)
`git rm log/\*.log`: \를 꼭 사용해야함. 

**다양한 git log 옵션들**
`-p`: 각 커밋의 패치
`--stat`: 각 커밋의 수정된 파일 통계정보
`--shortstat`: stat 명령어의 제한된 버전
`--name-only`: 커밋 정보 중 수정된 파일의 이름만
`--name-status`: 수정된 파일 목록 + 추가/수정/삭제한지 보여줌
`--abbrev-commit`: 체크섬 중 일부만 보여줌 (처음 몇자만)
`--relative-date`: 상대적인 형식(2 week ago)으로 날짜 표시
`--graph`
`--pretty`: 지정한 혁식으로 보여줌 (online, short, full, fuller, format)
=> format은 원하는 혁식으로 출력
`git log --since=2.weeks`: day 등으로 조회 가능
`git log --Sfuncion_name`: S옵션은 코드에서 추가/제거된 내용 중 특정 텍스트 포함
`git log --grep=html`을 사용해서 커밋 메세지 검색도 가능
`-(n)`: 최근 n개
`--since, --after`
`--until, --before`
`--author, --commiter`
`--grep, -S`

- 다양한 포멧 옵션들 (`git log --pretty=format:"%h - %an, %ar : %s"`)`
%H: 커밋해시
%h: 짧은해시
%T: 트리해시
%t: 짧은 트리해시
%P, %p: 부모해시
%an, ae, ad, ar: 각각 저자이름, 저자메일, 저자시각, 저자 상태시각
%cn, ce, cd, cr: 각각 커미터이름, 메일, 시각, 상대시각
%s: 요약


**되돌리기 기능들**
- staging area를 수정
`git commit --ammend`: staging area를 수정
- 파일 상태를 unstage로 변경
`git reset HEAD filename.txt`: unstage가 됨
> reset --hard를 사용하면 파일 수정된 내용도 사라짐 (워킹디렉토리도)
- modified 파일 되돌리기
`git checkout -- filename.txt`
> 꽤 위험한 명령... 수정한 내용이 전부 사라지고 원래 파일로 덮어써짐. (p.63)
> ch.3에서 다루는 내용을 사용하는것이 좋다...

**about remote**
`git fetch remote-name`: 리모트 저장소에서 데이터 가져오기

**git alias**(p.73)
추가한 alias들
`git config --global alias.br branch`
`git commit --global alias.st status`
`git commit --global alias.unstage 'reset HEAD --'`
`git commit --global alias.logm 'log --...'`
`git commit --global alias.last 'log -1 HEAD`
`git commit --global alias.cm commit`

## 03장. Git branch
Branch? diff가 아니라 snapshot으로 기록. 
`git branch` 명령어: 브랜치를 만들어줌. 
git은 작업중인 브랜치를 'HEAD'라는 특별한 포인터로 가르켜줌. 
`git log --decorate`: 브랜치가 어떤 커밋을 가르키는지 확인 가능.
`git checkout`으로 브랜치 이동: 브랜치가 이동하면서 하는 일은 두가지인데, master가 가르치는 커밋을 HEAD가 가르키게 하고 working directory의 파일도 그 시점으로 되돌려놓음. 
파일 변경시 문제가 발생해서 브랜치 이동이 불가능한 경우 checkout 명령어가 듣지 않음... 그래서 그랬구만.

`git ck -b issu53`으로 새로운 브랜치를 만들고 수정1
`git ck -b hotfix`로 새로운 브랜치를 만들고 수정2
`git ck master`: merge 할 branch로 이동
`git merge hotfix`: merge는 hotfix를 가져와서 master에 붙인다고 생각하면 될듯하다
> fast-forward?
> merge할 브랜치가 가르키는 커밋(hotfix)이 현 브랜치(master)의 upstream(직렬의? 바로 직행의) 브랜치이기 때문에 master branch pointer가 hotfix로 이동... 
> 즉, maerter를 가리키던 pointer(HEAD)가 hotfix가 있는 commit으로 이동할 뿐. 이를 *Fast forwad*라고 부름

이제 다시 issue53에서 수정을 한 뒤, master 브랜치에서 merge 해보자.
hotfix와는 다르게 fast-forward가 아닌, 공통 조상을 사용하여 3-way Merge를 한다.
=> 3-way merge의 결과를 별도의 커밋으로 만들고 해당 브랜치가 그 커밋을 가르키게 함.
=> 부모가 여러개, Merge commit이라고 부른다.:w

**충돌의 기초**
가끔 이런 3-way merge가 실패할때도 있음.
충돌이 일어난 파일은 unmerged
`git mergetool`: 다른 merge 도구로 충돌 해결가능. (mac에서는 opendiff)
=> 두 브랜치에서 같은 파일 수정, merge할 branch에서 같은 파일을 수정했으면 충돌 (master에서도 수정, hotfix에서도 수정하면...)
Q) hotfix, issue53에서 각각 수정하고 master에서 merge하면 충돌이 안나는데 마지막 merge를 가져오나?

**branch 관리**
`git branch -v`: 최근 커밋도 보여줌
`git branch --merged`, `git branch --no-merged`
`git branch -d testing`, `git branch -D testing`: merge 하지 않은 브랜치를 강제 삭제 (-D)

**다양한 브랜치 workflow**
- Long-Running 브랜치
배포할 코드만 master에 안정적으로 관리. 
개발 브렌치는 next나 develop로 만ㄹ들어서 사용. 
이후 각각의 토픽은 iss53같은짧은 호흡 브랜치를 만들어서 적용. 

**토픽 브랜치**
iss53, hotfix와 같이 특정 브랜치로 토픽을 관리

**리모트 브랜치**
`git remote -v`
리모트 브랜치 이름은 (remote)/(branch)형식 ex)`origin/master`
`git clone -o originname`으로 origin 대신 이름 부여 가능

리모트 서버에서 저장소 정보를 동기화하려면 `git fetch origin` 사용. 
=> origin 서버의 주소정보를 찾아 로컬의 저장소가 갖지 않은 새로운 정보를 내려받고 받은 데이터를 로컬 저장소에 업데이트 후 origin/master의 포인터 위치를 최신 커밋으로 이동..

**Push하기**
로컬 브랜치를 서버로 전송하려면 push. 
`git push (remote) (branch)`
`git push origin serverfix:awesomebranch`와 같이 remote 저장소의 이름을 줄 수 있음 (remote에서 다른 이름을 사용하는 경우)

만약 Fetch 명령으로 리모트 트래킹 브랜치를 내려받는다고 해서 새로운 브랜치가 생기는 것이 아님.
=> 단지 수정하지 못하는 origin/serverfix라는 브랜치가 생김. 이를 merge할수는 있다?
`git merge origin/serverfix`: 현재 branch에 remote branch를 merge
`git checkout -b serverfix origin`serverfix`: merge 하지 않고 새로운 리모트 브랜치에서 시작하는 branch 생성

**브랜치 추적하기**
remote tracking branch를 local branch로 ck하면 자동으로 tracking tranch 생성. (remote branch 와 직접 연결된 local branch)
예를들면 git clone을 했을 때 git은 자동으로 master를 origin/master의 tracking branch로 만듬.
`git checkout -b [branch] [remotename]/[branch]`로 다른 트래킹 브랜치를 만들 수 있음
`git checkout --track origin/serverfix`를 하면 local branch 이름을 자동으로 생성 (이경우 serverfix)

이미 로컬에 존재하는 브랜치가 특정 remote branch를 tracking하게 하려면 -u, --set-upstream-to 옵션을 붙여서
`git branch -u origin/serverfix`: -u가 이런 의미였구나..
> Upstream 별명
> tracking branch를 설정했다면 이를 @{upstream}, @{u}로 짧게 대체해서 사용 가능.
> `git merge origin/master`는 `git merge @{u}`와 같다.

`git branch -vv`로 remote branch와 함께 local branch가 앞서는지도 보여줌..? 왜 안되지... `git branch -r`?
=> 이 명령은 마지막 fetch 시점으로 계산.. 단순히 이 명령만으로는 최신 데이터 반영이 안됨. 
이를 위해 항상 최신 데이터를 받아온 후에 추적 상황 확인
`git fetch --all; git branch -vv`

**Pull하기**
`git fetch`: 서버에는 있고 local에는 없는 데이터 받아서 저장. working directory는 그대로. 나머지는 `git merge`를 해야함
`git pull`은 `git fetch`+`git pull`
> 일반적으로 fetch, merge를 명시적으로 사용하는 것이 pull보다 낫다!

**delete remote branch**
`git push origin --delete serverfix`로 remote branch를 삭제 가능. 이러면 서버에서 브랜치(커밋 포인터)가 사라짐 (???)
만약 local에는 있고 remote에는 없으면 how do I make remote branch 
