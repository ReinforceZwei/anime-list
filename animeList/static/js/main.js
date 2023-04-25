// function for get information and show

function getInfo(e, id) { // server get
    $.get('get/' + id, {}, function (e) {
        showInfo(e);
    });
}

function showInfo(anime) {
    t = {};
    t.animeName = $("#infoPanel #animeName");
    t.animeID = $("#infoPanel #animeID");
    t.addedTime = $("#infoPanel #addedTime");
    t.downloaded = $("#infoPanel #downloaded");
    t.watched = $("#infoPanel #watched");
    t.watchedTime = $("#infoPanel #watchedTime");
    t.estimateTime = $("#infoPanel #estimateTime");
    t.comment = $("#infoPanel #comment");
    t.rating = $("#infoPanel #rating");
    t.giveUp = $("#infoPanel #giveUp");
    t.url = $("#infoPanel #url");
    t.remark = $("#infoPanel #remark");
    t.tags = $("#infoPanel #tags");
    t.edit = $("#infoPanel #edit");

    t.edit.off('click');
    t.edit.click(function () {
        editInfo(anime)
    });
    
    let _watchedTime;
    let _addedTime = (new Date(anime.addedTime * 1000)).toLocaleString();
    //if(anime.watched!=0)let _watchedTime = (new Date(anime.watchedTime*1000)).toLocaleString();else let _watchedTime = "Not watched";
    if (anime.watched != 0) {
        // set mark watched hidden
        $("#markAsWatched").hide();
        $("#markAsUnwatched").show();
        // markAsUnwatched event handler
        $("#markAsUnwatched").off('click'); // clear last handler
        $("#markAsUnwatched").click(function () {
            markAsUnwatched(anime.animeID)
        });
        if (anime.watchedTime != 0) {
            _watchedTime = (new Date(anime.watchedTime * 1000)).toLocaleString();
        } else {
            _watchedTime = "沒有記錄";
        }
    } else {
        _watchedTime = "未觀看";
        $("#markAsWatched").show();
        $("#markAsUnwatched").hide();
        // markAsUnwatched event handler
        $("#markAsWatched").off('click'); // clear last handler
        $("#markAsWatched").click(function () {
            markAsWatched(anime.animeID)
        });
    }
    let estimateTime = -1;
    let diff;
    if (anime.watched == "1") {
        let prevWatchedTime = $(`#id-${anime.animeID}`).parent().prev().children().attr('data-watched-time')
        if (prevWatchedTime !== undefined){
            diff = Number.parseInt(anime.watchedTime) - Number.parseInt(prevWatchedTime);
            if (Number.parseInt(prevWatchedTime) === 0 || diff == 0){
                estimateTime = "無法估計";
            } else {
                estimateTime = Math.round(diff / (3600 * 24)) + "日";
            }
        }else{
            estimateTime = "這是第一部"
        }
    }
    if (estimateTime === -1) estimateTime = "未觀看";
    t.animeName.text(anime.animeName);
    t.animeID.text(anime.animeID);
    t.addedTime.text(_addedTime);
    t.downloaded.text(anime.downloaded != 0 ? "是" : "否");
    t.watched.text(anime.watched != 0 ? "是" : "否");
    t.watchedTime.text(_watchedTime);
    t.estimateTime.text(estimateTime);
    t.comment.text(anime.comment ? anime.comment : '');
    t.url.text(linkify(anime.url ? anime.url : ""));
    t.remark.text(anime.remark);
    t.tags.text(anime.tags.join(','));

    if (anime.rating == -1) {
        t.rating.hide();
        t.giveUp.show();
    } else {
        t.giveUp.hide();
        t.rating.show();
        t.rating.rateit({
            step: 1,
            readonly: true
        });
        t.rating.rateit('value', anime.rating);
    }

    $("#animeNameCopy").val(anime.animeName);

    showInfoPanel();

    tmdb.smartSearch(anime.animeName)
    .then(e=>{
        console.log(e)
        $("#infoPanel").css('background-image', `url(${e[0]})`)
        $(".cover-viewer img").attr('src', e[0])
    })
    .catch(() => {
        $("#infoPanel").css('background-image', '');
        $(".cover-viewer img").attr('src', '')
    })
}

function _addAnime() {
    let name = prompt("請輸入名稱");
    if (name) {
        addAnime(name);
    }
}

function addAnime(animeName) {
    let data = {
        "animeName": animeName
    };
    //alert(data.animeName);
    $.post('add', data, function (e) {
        addNewItem(animeName, e.animeID);
        scrollToBottom();
    })
    .fail(function (e) {
        alert("fail\r\nMaybe record already exist?")
    });
}

function editInfo(anime) {
    t = {};
    t.animeName = $("#editPanel #animeName");
    t.animeID = $("#editPanel #animeID");
    t.addedTime = $("#editPanel #addedTime");
    t.downloaded = $("#editPanel #downloaded");
    t.watched = $("#editPanel #watched");
    t.watchedTime = $("#editPanel #watchedTime");
    t.comment = $("#editPanel #comment");
    t.rating = $("#editPanel #rating");
    t.giveUp = $("#editPanel #giveUp");
    t.url = $("#editPanel #url");
    t.remark = $("#editPanel #remark");
    t.tags = $("#editPanel #tags");
    t.save = $("#editPanel #saveButtom");

    t.save.off('click');
    t.save.click(function () {
        _saveInfo(anime.animeID, anime)
    });

    let _watchedTime;
    let _addedTime = (new Date(anime.addedTime * 1000)).toLocaleString();
    //if(anime.watched!=0)let _watchedTime = (new Date(anime.watchedTime*1000)).toLocaleString();else let _watchedTime = "Not watched";
    if (anime.watched != 0) {
        if (anime.watchedTime != 0) {
            _watchedTime = (new Date(anime.watchedTime * 1000)).toLocaleString();
        } else {
            _watchedTime = "沒有記錄";
        }
    } else {
        _watchedTime = "未觀看";
    }
    t.animeName.val(anime.animeName);
    t.downloaded.prop('checked', anime.downloaded != 0);
    t.comment.val(anime.comment);
    t.url.val(anime.url);
    t.remark.val(anime.remark);
    t.tags.val(anime.tags.join(','));

    if (anime.rating == -1) {
        t.giveUp.prop('checked', true);
    }
    t.rating.rateit({
        step: 1
    });
    t.rating.rateit('value', anime.rating);

    t.watched.text(anime.watched != 0 ? "是" : "否");
    t.watchedTime.text(_watchedTime);
    t.animeID.text(anime.animeID);
    t.addedTime.text(_addedTime);

    showEditPanel();
}

function _saveInfo(id, original) {
    t = {};
    t.animeName = $("#editPanel #animeName");
    t.animeID = $("#editPanel #animeID");
    t.addedTime = $("#editPanel #addedTime");
    t.downloaded = $("#editPanel #downloaded");
    t.watched = $("#editPanel #watched");
    t.watchedTime = $("#editPanel #watchedTime");
    t.comment = $("#editPanel #comment");
    t.rating = $("#editPanel #rating");
    t.giveUp = $("#editPanel #giveUp");
    t.url = $("#editPanel #url");
    t.remark = $("#editPanel #remark");
    t.tags = $("#editPanel #tags");

    let anime = {};
    anime.animeID = id; //t.animeID.html();
    anime.animeName = t.animeName.val();
    anime.downloaded = t.downloaded.prop('checked');
    anime.comment = t.comment.val();
    anime.rating = t.rating.rateit('value');
    anime.url = t.url.val();
    anime.remark = t.remark.val();
    anime.tags = t.tags.val().replace(/[\uff0c]/g, ",").split(',');

    if (t.giveUp.prop('checked')) {
        anime.rating = -1;
    }

    saveInfo(anime, original);
}

function saveInfo(anime, original) {
    console.log(anime);
    update(anime.animeID, anime, ()=>{
        closeEditPanel();
        original = Object.assign(original, anime)
        showInfo(original);
        updateItem(original);
    });
}

function _search() {
    let string = $("#searchInput").val();
    if (string === '' || string === ' ') {
        $("#searchResult").empty();
        return;
    }
    let field = $("#searchByTag").prop('checked') ? "tags" : "animeName";
    local_search(string, animes, field, function (e) {
        //let anime = JSON.parse(e);
        let anime = e;
        let node = $("#searchResult");
        //console.log(anime);
        node.empty();
        if (anime.length == 0) {
            node.append('<div class="search__item">沒有結果</div>');
            return;
        }
        anime.forEach((e, i) => {
            //console.log(e);
            let code = `<div class="search__item" onclick="findOnPage(${e.animeID})">${e.animeName}</div>`;
            node.append(code);
        });
    });
}
function search(string, callback) {
    $.get('search', { "q": string }, function (e) { console.log(e); callback(e) });
}
function local_search(string, objects, field, callback) {
    //search without requesting server everytime
    var results = [];
    string = string.toLowerCase();
    for (var i = 0; i < objects.length; i++) {
        if (Array.isArray(objects[i][field])) {
            // is a Array
            objects[i][field].forEach((e, j) => {
                if (objects[i][field][j].toLowerCase().indexOf(string) != -1) {
                    results.push(objects[i]);
                }
            });
        } else {
            if (objects[i][field].toLowerCase().indexOf(string) != -1) {
                results.push(objects[i]);
            }
        }
    }
    if (callback) callback(results);
    return results;
} 
function update(id, arr, callback) {
    $.post('update/' + id, arr, function () {
        if(typeof(callback) == 'function') callback();
    })
    .fail(err=>{console.log(err)});
} 
function findOnPage(id) {
    hideSearchBar();
    $([document.documentElement, document.body]).animate({
        scrollTop: $("#id-" + id).offset().top - 200
    }, 400, function () {
        blink(id);
    });
} 
function scrollToBottom() {
    $([document.documentElement, document.body]).animate({
        scrollTop: $(document).height()
    }, 400);
} 
function markAsWatched(id) {
    let data = {
        "watched": 1,
        "watchedTime": Math.floor(Date.now() / 1000)
    };
    //alert(data.animeID);
    $.post('update/' + id, data, function (e) {
        $(`#id-${id}`).parent().appendTo('#list-watched');
        findOnPage(id);
        getInfo(undefined, id);
    });
} 
function markAsUnwatched(id) {
    let data = {
        "watched": "0",
        "watchedTime": 0
    };
    //alert(data.animeID);
    $.post('update/' + id, data, function (e) {
        localStorage.setItem('next', 'focus');
        localStorage.setItem('id', id);
        location.reload();
    });
} 
function handleNext() {
    //let next = getParameterByName('next');
    let next = localStorage.getItem('next');
    let id = 0;
    if (next) {
        switch (next) {
            case 'info':
                // open infoPanel
                id = localStorage.getItem('id');
                if (id) {
                    //findOnPage(id);
                    showInfo(animeListByID[Number.parseInt(id)]);
                }
                break;
            case 'focus':
                // jump to item
                id = localStorage.getItem('id');
                if (id) {
                    findOnPage(id);
                }
                break;
            case 'bottom':
                // jump to bottom
                scrollToBottom();
                break;
        }
        localStorage.removeItem('next');
        localStorage.removeItem('id');
    }
}

function addNewItem(animeName, animeID){
    let l = $("#list-unwatched");
    let lastChild = l.children().last();
    l.children().last().remove();
    
    let id = animeID;
    let item = (`
        <li>
            <a onclick="getInfo(event,${id})" id="id-${id}">${animeName}<span class="remark"></span></a>
        </li>
    `)
    l.append(item);
    
    l.append(lastChild)
}

function updateItem(anime){
    let item = $(`#id-${anime.animeID}`);
    let className = '';
    if (anime.watched == 1) className += ' watched';
    if (anime.downloaded == 1) className += ' downloaded';
    if (anime.rating == -1) className += ' deleteLine'
    item[0].children[0].innerText = anime.remark ? `（${anime.remark}）` : '';
    item[0].setAttribute('class', className)
}
//for view and other function

function closeInfoPanel() {
    $("#infoPanel").hide();
} 
function showInfoPanel() {
    $("#infoPanel").show();
} 
function closeEditPanel() {
    $("#editPanel").hide();
} 
function showEditPanel() {
    $("#editPanel").show();
} 
function hideSearchBar() {
    $("#searchResult").empty();
    $(".search").removeClass('search--active')
    $('.magnifier').removeClass('magnifier--active')
} 
function showSearchBar() {
    $(".search").addClass('search--active');
    $('.magnifier').addClass('magnifier--active')
    $("#searchInput").focus();
    _search();
}
function toggleSearchBar() {
    if ($(".search").hasClass('search--active')) {
        hideSearchBar()
    }else{
        showSearchBar()
    }
}
function toggleDarkMode() {
    if (!mode) {
        // dark
        darkModeOn();
    } else {
        // light
        darkModeOff();
    }
} 
function darkModeOn() {
    $("link#darkMode")[0].rel = "stylesheet";
    localStorage.setItem('darkMode', 1);
    mode = 1;
} 
function darkModeOff() {
    $("link#darkMode")[0].rel = "alternate stylesheet";
    localStorage.setItem('darkMode', 0);
    mode = 0;
} 

function showCover(){
    $(".cover-viewer").show();
}
function closeCover(){
    $(".cover-viewer").hide();
}
function toggleDropdown() {
    $('.hamburger').toggleClass("hamburger--change");
    $('.dropdown__content').toggleClass('dropdown__content--active');
    $('.dropdown__item').each(function (i, el) {
      	$(el).css('--n', i + 1);
    });
}

function copyNameToClipboard() {
    var copyText = document.getElementById("animeNameCopy");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand('copy');
} 
function blink(id) {
    let node = $("#id-" + id);
    node.css('background-color', 'yellow');
    setTimeout(function () {
        node.css('background-color', '');
    }, 1000);
} 
function delay(fn, ms) {
    let timer = 0
    return function (...args) {
        clearTimeout(timer)
        timer = setTimeout(fn.bind(this, ...args), ms || 0)
    }
} 
function ToCDB(str) {
    var tmp = "";
    for (var i = 0; i < str.length; i++) {
        if (str.charCodeAt(i) == 12288) {
            tmp += String.fromCharCode(str.charCodeAt(i) - 12256);
            continue;
        }
        if (str.charCodeAt(i) > 65280 && str.charCodeAt(i) < 65375) {
            tmp += String.fromCharCode(str.charCodeAt(i) - 65248);
        } else {
            tmp += String.fromCharCode(str.charCodeAt(i));
        }
    }
    return tmp
} 
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
} 
function redirect(page) {
    window.location.href = '/anime/' + page;
} 
function enableStylesheet(node) {
    node.rel = 'stylesheet';
} 
function disableStylesheet(node) {
    node.rel = 'alternate stylesheet';
}
function linkify(text) {
    return text.replace(urlRegex, function(url) {
        return '<a href="' + url + '">' + decodeURIComponent(url) + '</a>';
    });
}

function makeSearchCache() {
    // Extract name list from DOM for local searching
    animes = [];
    $('.animeList li a').each((i, e) => {
        let o = {
            'animeName': e.text,
            'animeID': Number(e.id.replace('id-',''))
        }
        animes.push(o)
    })
    animes.sort((a, b) => a.animeName < b.animeName ? -1 : 1)
}
// global var declear

// Deprecated variables
//var animeList;
//var animeListByID = [];

var animes = [];

var urlRegex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;()]*[-A-Z0-9+&@#\/%=~_|()])/gi;
/** This part will be handled by caching. To Be Removed

$.get('get', {}, function (e) {
    animeList = JSON.parse(e);
    animeList.forEach((e, i) => {
        animeListByID[e.animeID] = e;
    });
    onDataLoad();
});
*/

/* Init Dark mode */
var mode = localStorage.getItem('darkMode') == true ? 0 : 1; toggleDarkMode();

/* on data available */
function onDataLoad() {
    handleNext();
}

/* on scroll event */
var prevScrollpos = window.pageYOffset;
var scrollTimer, lastScrollFireTime = 0;
var hidden = false;
var _onScroll = function () {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        // show
        if (hidden) {
            $(".reload").show();
            $(".toggleSearch").show();
            hidden = false;
        }
    } else {
        // hide
        if (!hidden) {
            $(".reload").hide();
            $(".toggleSearch").hide();
            hidden = true;
        }
    }
    prevScrollpos = currentScrollPos;
}
// $(window).on('scroll', function () {
//     var minScrollTime = 100;
//     var now = new Date().getTime();

//     function processScroll() {
//         _onScroll();
//     }

//     if (!scrollTimer) {
//         if (now - lastScrollFireTime > (3 * minScrollTime)) {
//             processScroll(); // fire immediately on first scroll
//             lastScrollFireTime = now;
//         }
//         scrollTimer = setTimeout(function () {
//             scrollTimer = null;
//             lastScrollFireTime = new Date().getTime();
//             processScroll();
//         }, minScrollTime);
//     }
// });
//window.onscroll = _onScroll;
// on ready function
$(document).ready(function () {
    closeInfoPanel();
    closeEditPanel();
    hideSearchBar();
    $("#searchInput").on('keyup input', delay(function (e) {
        _search();
    }, 300));
    $("#view-cover").on('click', () => {showCover()});
    $(".cover-viewer img").on('click', () => {closeCover()});

    makeSearchCache()
    onDataLoad();
    // Caching is removed
    indexedDB.deleteDatabase('AnimeDB');
});