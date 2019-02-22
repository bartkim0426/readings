## 2장. 이름에 정보 담기

#### 예시

- `get`과 같은 무의미안 단어 피하기
- v15_www 리팩토링 예시

```python
def program_list_view(request, category_slug):
    ...
    page_title = get_page_title(category_slug)

    return render(request, "webapp/program_list.html", context={
    ...
    })

...

def get_page_title(category_slug):
	"""
	category_slug => (조건에 따라) "Korean {category_slug} - OnDemandKorea" 로 title 포매팅
	"""
    tmp_title = _(category_slug.title())
    if any(keyword in tmp_title for keyword in ["Drama", "Variety", "Documentary"]):
        tmp_title = f"Korean {tmp_title}"

    return f"{tmp_title} - OnDemandKorea"
```

- page_title을 가져오는 `get_page_title`?
- `page_title`이 모호? html title tag를 명확히 나타내주지 못함
- get? 어디서 가져오는지, 기존에 존재하는 값인지 등이 모호함
- generate, create / 아니면 단순 포메팅이기 때문에 format, trim 도 괜찮을 듯 하지만 헷갈릴 우려도 있음
- `(category_slug)`를 인자로 받으므로 suffix로 `_from`을 넣어주는 것도 좋을듯
- `page_title` 대신 `html_page_title`, `html_title`도 고려 (실제로는 기존에 쓰는 값이 `page_title`이기 때문에 통일성을 고려)

그래서 나온 후보군은

```
# generate이지만 완전 생성은 아님
generate_html_title_from(category_slug)

# 포멧 => 초기화의 느낌이 조금 남
format_html_title_from(category_slug)

# trim => 단어가 직관적이지 않음
trim_html_title_from(category_slug)
```

> Alfred powerpack을 사용중이라면 synonyms/antonyms 검색하는 `alfred-powerthesaururs` workflow (https://github.com/clarencecastillo/alfred-powerthesaurus) 사용해봐도 좋을듯


**약어 잘 못 쓴 예**
- 득정 프로젝트에 국한된 의미 => 새로 합류한 사람에게 비밀스럽고 위협 (`WpAll, WpMeta.....`)
- `WpAll`, `WpMeta`... -> 처음 왔을 떄 무슨 말인지 전혀 감이 안 잡힘
- 또한 `All`, `Meta`도 해당 클래스를 제대로 나타내주지 못함
- legacy임을 드러낼 수 있게 `Legacy`를 붙여도 좋았을 듯


**context 예시 (episode_view)**

```python
context_dict = {
    "program": prog,
    "episode": episode,
    "is_expired": episode.post_status == "expired",
    "video_hls_url": video_hls_url,
    "video_mp4_url": video_mp4_url,
    "page_title": f"{episode.localized_post_title} - OnDemandKorea",
    "latest_contents": latest_contents,
    "plus_only": is_plus_episode,
    "captions": available_captions_with_host_prefix,
    "continue_watching_position": request.GET.get("pos", 0),
    "category_slug": episode.parent_name if episode.parent_name else "",
    "do_bypass_ppv_purchase": do_bypass_ppv_purchase,
    "date_showing": (prog.get_postmeta("not_showing_date") != "1" and prog.get_postmeta("onair") != "0"),
    "admap": admap,
    "desktop_ads_tag": desktop_ads_tag,
    "show_embeded_copy_button": False,
    "play_id": play_id,
    "odk_id": request.odk_id,
    "is_bot": is_bot(request),
    "ref_id": article_id,
    "ref_type": category_name,
    "encoded_ref_url": urlquote_plus(referer_url),
    "ref_host": urlquote_plus(parsed_referer_url.netloc.lower()),
    "is_playing_on_air_date": (episode.on_air_date == local_now.strftime("%m/%d/%Y")),
    "player_feature": player_feature,
    "is_region_blocked": is_region_blocked,
    "is_access_from_odk_office": is_access_from_odk_office,
    "is_test_facebook_ads": is_test_facebook_ads,
    "is_npaw_enabled": settings.IS_NPAW_ENABLED,
    "do_show_context": get_adhoc_param(request, "do_show_context"),
    "is_no_overlay": get_adhoc_param(request, "is_no_overlay"),
    "adhoc_params": request.adhoc_params,
    "is_kpop": is_kpop,
    "is_peer5_enabled": is_peer5_enabled
}
```

- `plus_only`: True/False 반환하므로 `is_plus_only` 사용하면 좋을듯
- `do_bypass_ppv_purchase`, `do_show_context`: `do`로 시작해서 무슨 말인지 잘 모르겠음. 정확한 뜻을 내포하는 단어 적어주면 좋을듯.
