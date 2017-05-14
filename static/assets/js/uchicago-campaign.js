
var siteURL = "campaign.uchicago.edu";
if (function($) {
        $.fn.GSASearch = function(t) {
            function e(e, o, r, a, l) {
                var u = {
                        _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
                        encode: function(t) {
                            var e = "",
                                i, n, o, s, r, a, l, c = 0;
                            for (t = u._utf8_encode(t); c < t.length;) i = t.charCodeAt(c++), n = t.charCodeAt(c++), o = t.charCodeAt(c++), s = i >> 2, r = (3 & i) << 4 | n >> 4, a = (15 & n) << 2 | o >> 6, l = 63 & o, isNaN(n) ? a = l = 64 : isNaN(o) && (l = 64), e = e + this._keyStr.charAt(s) + this._keyStr.charAt(r) + this._keyStr.charAt(a) + this._keyStr.charAt(l);
                            return e
                        },
                        decode: function(t) {
                            var e = "",
                                i, n, o, s, r, a, l, c = 0;
                            for (t = t.replace(/[^A-Za-z0-9\+\/\=]/g, ""); c < t.length;) s = this._keyStr.indexOf(t.charAt(c++)), r = this._keyStr.indexOf(t.charAt(c++)), a = this._keyStr.indexOf(t.charAt(c++)), l = this._keyStr.indexOf(t.charAt(c++)), i = s << 2 | r >> 4, n = (15 & r) << 4 | a >> 2, o = (3 & a) << 6 | l, e += String.fromCharCode(i), 64 != a && (e += String.fromCharCode(n)), 64 != l && (e += String.fromCharCode(o));
                            return e = u._utf8_decode(e)
                        },
                        _utf8_encode: function(t) {
                            t = t.replace(/\r\n/g, "\n");
                            for (var e = "", i = 0; i < t.length; i++) {
                                var n = t.charCodeAt(i);
                                128 > n ? e += String.fromCharCode(n) : n > 127 && 2048 > n ? (e += String.fromCharCode(n >> 6 | 192), e += String.fromCharCode(63 & n | 128)) : (e += String.fromCharCode(n >> 12 | 224), e += String.fromCharCode(n >> 6 & 63 | 128), e += String.fromCharCode(63 & n | 128))
                            }
                            return e
                        },
                        _utf8_decode: function(t) {
                            for (var e = "", i = 0, n = c1 = c2 = 0; i < t.length;) n = t.charCodeAt(i), 128 > n ? (e += String.fromCharCode(n), i++) : n > 191 && 224 > n ? (c2 = t.charCodeAt(i + 1), e += String.fromCharCode((31 & n) << 6 | 63 & c2), i += 2) : (c2 = t.charCodeAt(i + 1), c3 = t.charCodeAt(i + 2), e += String.fromCharCode((15 & n) << 12 | (63 & c2) << 6 | 63 & c3), i += 3);
                            return e
                        }
                    },
                    c = "&q=" + escape(e) + "&start=" + escape(o) + "&sitesearch=" + escape(a) + "&site=" + escape(l);
                c += "&filter=0";
                var h = "btnG=Search&entqr=0&ud=1&sort=date%3AD%3AL%3Ad1&output=xml_no_dtd&oe=UTF-8&ie=UTF-8&client=default_frontend&proxystylesheet=jsonp_frontend" + c + "&num=" + escape(r),
                    d = t.protocol + "//search.uchicago.edu/search?btnG=Search&entqr=0&ud=1&sort=date:D:L:d1&output=xml_no_dtd&oe=UTF-8&ie=UTF-8&client=default_frontend&proxystylesheet=default_frontend" + c,
                    p = t.protocol + "//webresources.uchicago.edu/php/proxy/gsaproxy.php?encodedParams=" + u.encode(h) + "&callback=?";
                s.data("searchSiteURL", d);
                var f = 0,
                    m = $.getJSON(p, function(t) {
                        n(t), f = 1
                    });
                void 0 != m ? m.error(function() {
                    i()
                }) : setTimeout(function() {
                    f || i()
                }, 7e3)
            }

            function i() {
                var t = 'There is a problem fetching search results. Please refresh the page or contact <a href="mailto:weberror@uchicago.edu">weberror@uchicago.edu</a>.';
                s.html(t), s.data("totalCount", 0), s.trigger("GSASearchComplete")
            }

            function n(e) {
                var i, n = 0,
                    o = "<h2>You searched for: <strong>" + e.GSP.Q + "</strong></h2>";
                if (void 0 == e.GSP.RES) o += "<p>No pages were found.</p>";
                else {
                    o += "<p><strong>Results " + e.GSP.RES.SN + " - " + e.GSP.RES.EN + " of about " + e.GSP.RES.M + ".</strong></p>";
                    var r = e.GSP.RES.EN - e.GSP.RES.SN + 1;
                    if (1 == r) {
                        var a = e.GSP.RES.R;
                        null == a.S && (a.S = "");
                        var l = '<h3><a href="' + a.U + '">' + a.T + "</a></h3>";
                        l += "<p>" + a.S + "<br><em>" + a.U + "</em></p>", o += l
                    } else
                        for (var u = 0; r > u; u++) {
                            var a = e.GSP.RES.R[u];
                            null == a.S && (a.S = "");
                            var l = '<h3><a href="' + a.U + '">' + a.T + "</a></h3>";
                            l += "<p>" + a.S + "<br><em>" + a.U + "</em></p>", o += l
                        }
                    var c = t.num;
                    i = e.GSP.RES.SN, n = c > r ? e.GSP.RES.EN : e.GSP.RES.M
                }
                s.html(o), s.data("startNumber", i), s.data("totalCount", n), s.trigger("GSASearchComplete")
            }
            var o = {
                    q: "",
                    start: "",
                    num: "10",
                    sitesearch: "",
                    site: "default_collection",
                    waitGifPath: "/i/template/loading.gif",
                    protocol: location.protocol
                },
                t = $.extend(o, t),
                s = $(this);
            return s.data("searchSiteURL", t.protocol + "//search.uchicago.edu"), s.data("startNumber", "1"), s.data("totalCount", "10"), this.each(function() {
                s.empty(), s.html('<img src="' + t.waitGifPath + '" class="GSAwait">'), t.q = t.q.replace(/(<([^>]+)>)/gi, ""), t.start = t.start.toString().replace(/(<([^>]+)>)/gi, ""), t.num = t.num.toString().replace(/(<([^>]+)>)/gi, ""), t.sitesearch = t.sitesearch.replace(/(<([^>]+)>)/gi, ""), t.site = t.site.replace(/(<([^>]+)>)/gi, ""), e(t.q, t.start, t.num, t.sitesearch, t.site)
            })
        }
    }(jQuery), function($) {
        function t(t, i, n) {
            var o = $("<ul></ul>");
            o.append(e("First", t, i, n));
            var s = 1,
                r = 9;
            t > 4 && (s = t - 4, r = t + 4), r > i && (s = i - 8, r = i), 1 > s && (s = 1);
            for (var a = s; r >= a; a++) {
                var l = $("<li>" + a + "</li>");
                a == t ? l.addClass("active") : l.bind("click focusin", function() {
                    n(this.firstChild.data)
                }), l.appendTo(o)
            }
            return o.append(e("Last", t, i, n)), o
        }

        function e(t, e, i, n) {
            var o = $("<li>" + t + "</li>"),
                s = 1;
            switch (t) {
                case "first":
                    s = 1;
                    break;
                case "last":
                    s = i
            }
            return "first" == t ? 1 >= e ? o : o.bind("click focusin", function() {
                n(s)
            }) : e >= i ? o : o.bind("click focusin", function() {
                n(s)
            }), o
        }
        $.fn.pager = function(e) {
            var i = $.extend({}, $.fn.pager.defaults, e);
            return this.each(function() {
                $(this).empty().append(t(parseInt(e.pagenumber), parseInt(e.pagecount), e.buttonClickCallback))
            })
        }, $.fn.pager.defaults = {
            pagenumber: 1,
            pagecount: 1
        }
    }(jQuery), $(document).ready(function() {
        function t(t) {
            linkDiv = $("#GSALink"), pagerDiv = $("#GSAPager"), resultsDiv = $("#GSAResults"), thisQ = t, perPageCount = 15, linkDiv.empty(), pagerDiv.empty(), resultsDiv.GSASearch({
                q: thisQ,
                num: perPageCount,
                sitesearch: siteURL
            })
        }

        function e() {
            var t;
            for (queryString = window.location.search.substring(1), nameValPairs = queryString.split("&"), i = 0; i < nameValPairs.length; i++) nameVal = nameValPairs[i].split("="), "GSAq" == nameVal[0] && (t = nameVal[1]);
            return t
        }
        var n = e();
        void 0 != e() && (n = unescape(n), t(n)), $("#GSAResults").bind("GSASearchComplete", function() {
            pagerDiv = $("#GSAPager"), perPageCount = 15, resultsDiv = $(this), pagerDiv.empty(), thisPageNumber = Math.floor((parseInt(resultsDiv.data("startNumber")) + parseInt(perPageCount)) / parseInt(perPageCount)), thisPageCount = Math.ceil(parseInt(resultsDiv.data("totalCount")) / perPageCount), pagerDiv.pager({
                pagenumber: thisPageNumber,
                pagecount: thisPageCount,
                buttonClickCallback: PagerClick
            })
        }), PagerClick = function(t) {
            resultsDiv = $("#GSAResults"), perPageCount = 15, startNumber = t * perPageCount - perPageCount, resultsDiv.GSASearch({
                q: n,
                start: startNumber,
                num: perPageCount,
                sitesearch: siteURL
            })
        }
    }), function($) {
        $.fn.hoverIntent = function(t, e) {
            var i = {
                sensitivity: 7,
                interval: 100,
                timeout: 0
            };
            i = $.extend(i, e ? {
                over: t,
                out: e
            } : t);
            var n, o, s, r, a = function(t) {
                    n = t.pageX, o = t.pageY
                },
                l = function(t, e) {
                    return e.hoverIntent_t = clearTimeout(e.hoverIntent_t), Math.abs(s - n) + Math.abs(r - o) < i.sensitivity ? ($(e).off("mousemove", a), e.hoverIntent_s = 1, i.over.apply(e, [t])) : (s = n, r = o, e.hoverIntent_t = setTimeout(function() {
                        l(t, e)
                    }, i.interval), void 0)
                },
                u = function(t, e) {
                    return e.hoverIntent_t = clearTimeout(e.hoverIntent_t), e.hoverIntent_s = 0, i.out.apply(e, [t])
                },
                c = function(t) {
                    var e = jQuery.extend({}, t),
                        n = this;
                    n.hoverIntent_t && (n.hoverIntent_t = clearTimeout(n.hoverIntent_t)), "mouseenter" == t.type ? (s = e.pageX, r = e.pageY, $(n).on("mousemove", a), 1 != n.hoverIntent_s && (n.hoverIntent_t = setTimeout(function() {
                        l(e, n)
                    }, i.interval))) : ($(n).off("mousemove", a), 1 == n.hoverIntent_s && (n.hoverIntent_t = setTimeout(function() {
                        u(e, n)
                    }, i.timeout)))
                };
            return this.on("mouseenter", c).on("mouseleave", c)
        }
    }(jQuery), function($, t, e, i) {
        var n = $(t);
        $.fn.lazyload = function(o) {
            function s() {
                var t = 0;
                r.each(function() {
                    var e = $(this);
                    if (!l.skip_invisible || e.is(":visible"))
                        if ($.abovethetop(this, l) || $.leftofbegin(this, l));
                        else if ($.belowthefold(this, l) || $.rightoffold(this, l)) {
                        if (++t > l.failure_limit) return !1
                    } else e.trigger("appear"), t = 0
                })
            }
            var r = this,
                a, l = {
                    threshold: 0,
                    failure_limit: 0,
                    event: "scroll",
                    effect: "show",
                    container: t,
                    data_attribute: "original",
                    skip_invisible: !0,
                    appear: null,
                    load: null,
                    placeholder: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC"
                };
            return o && (i !== o.failurelimit && (o.failure_limit = o.failurelimit, delete o.failurelimit), i !== o.effectspeed && (o.effect_speed = o.effectspeed, delete o.effectspeed), $.extend(l, o)), a = l.container === i || l.container === t ? n : $(l.container), 0 === l.event.indexOf("scroll") && a.bind(l.event, function() {
                return s()
            }), this.each(function() {
                var t = this,
                    e = $(t);
                t.loaded = !1, (e.attr("src") === i || e.attr("src") === !1) && e.is("img") && e.attr("src", l.placeholder), e.one("appear", function() {
                    if (!this.loaded) {
                        if (l.appear) {
                            var i = r.length;
                            l.appear.call(t, i, l)
                        }
                        $("<img />").bind("load", function() {
                            var i = e.attr("data-" + l.data_attribute);
                            e.hide(), e.is("img") ? e.attr("src", i) : e.css("background-image", "url('" + i + "')"), e[l.effect](l.effect_speed), t.loaded = !0;
                            var n = $.grep(r, function(t) {
                                return !t.loaded
                            });
                            if (r = $(n), l.load) {
                                var o = r.length;
                                l.load.call(t, o, l)
                            }
                        }).attr("src", e.attr("data-" + l.data_attribute))
                    }
                }), 0 !== l.event.indexOf("scroll") && e.bind(l.event, function() {
                    t.loaded || e.trigger("appear")
                })
            }), n.bind("resize", function() {
                s()
            }), /(?:iphone|ipod|ipad).*os 5/gi.test(navigator.appVersion) && n.bind("pageshow", function(t) {
                t.originalEvent && t.originalEvent.persisted && r.each(function() {
                    $(this).trigger("appear")
                })
            }), $(e).ready(function() {
                s()
            }), this
        }, $.belowthefold = function(e, o) {
            var s;
            return s = o.container === i || o.container === t ? (t.innerHeight ? t.innerHeight : n.height()) + n.scrollTop() : $(o.container).offset().top + $(o.container).height(), s <= $(e).offset().top - o.threshold
        }, $.rightoffold = function(e, o) {
            var s;
            return s = o.container === i || o.container === t ? n.width() + n.scrollLeft() : $(o.container).offset().left + $(o.container).width(), s <= $(e).offset().left - o.threshold
        }, $.abovethetop = function(e, o) {
            var s;
            return s = o.container === i || o.container === t ? n.scrollTop() : $(o.container).offset().top, s >= $(e).offset().top + o.threshold + $(e).height()
        }, $.leftofbegin = function(e, o) {
            var s;
            return s = o.container === i || o.container === t ? n.scrollLeft() : $(o.container).offset().left, s >= $(e).offset().left + o.threshold + $(e).width()
        }, $.inviewport = function(t, e) {
            return !($.rightoffold(t, e) || $.leftofbegin(t, e) || $.belowthefold(t, e) || $.abovethetop(t, e))
        }, $.extend($.expr[":"], {
            "below-the-fold": function(t) {
                return $.belowthefold(t, {
                    threshold: 0
                })
            },
            "above-the-top": function(t) {
                return !$.belowthefold(t, {
                    threshold: 0
                })
            },
            "right-of-screen": function(t) {
                return $.rightoffold(t, {
                    threshold: 0
                })
            },
            "left-of-screen": function(t) {
                return !$.rightoffold(t, {
                    threshold: 0
                })
            },
            "in-viewport": function(t) {
                return $.inviewport(t, {
                    threshold: 0
                })
            },
            "above-the-fold": function(t) {
                return !$.belowthefold(t, {
                    threshold: 0
                })
            },
            "right-of-fold": function(t) {
                return $.rightoffold(t, {
                    threshold: 0
                })
            },
            "left-of-fold": function(t) {
                return !$.rightoffold(t, {
                    threshold: 0
                })
            }
        })
    }(jQuery, window, document), "undefined" == typeof jQuery) throw new Error("Bootstrap's JavaScript requires jQuery"); + function($) {
    "use strict";

    function t(t) {
        return this.each(function() {
            var i = $(this),
                n = i.data("bs.button"),
                o = "object" == typeof t && t;
            n || i.data("bs.button", n = new e(this, o)), "toggle" == t ? n.toggle() : t && n.setState(t)
        })
    }
    var e = function(t, i) {
        this.$element = $(t), this.options = $.extend({}, e.DEFAULTS, i), this.isLoading = !1
    };
    e.VERSION = "3.2.0", e.DEFAULTS = {
        loadingText: "loading..."
    }, e.prototype.setState = function(t) {
        var e = "disabled",
            i = this.$element,
            n = i.is("input") ? "val" : "html",
            o = i.data();
        t += "Text", null == o.resetText && i.data("resetText", i[n]()), i[n](null == o[t] ? this.options[t] : o[t]), setTimeout($.proxy(function() {
            "loadingText" == t ? (this.isLoading = !0, i.addClass(e).attr(e, e)) : this.isLoading && (this.isLoading = !1, i.removeClass(e).removeAttr(e))
        }, this), 0)
    }, e.prototype.toggle = function() {
        var t = !0,
            e = this.$element.closest('[data-toggle="buttons"]');
        if (e.length) {
            var i = this.$element.find("input");
            "radio" == i.prop("type") && (i.prop("checked") && this.$element.hasClass("active") ? t = !1 : e.find(".active").removeClass("active")), t && i.prop("checked", !this.$element.hasClass("active")).trigger("change")
        }
        t && this.$element.toggleClass("active")
    };
    var i = $.fn.button;
    $.fn.button = t, $.fn.button.Constructor = e, $.fn.button.noConflict = function() {
        return $.fn.button = i, this
    }, $(document).on("click.bs.button.data-api", '[data-toggle^="button"]', function(e) {
        var i = $(e.target);
        i.hasClass("btn") || (i = i.closest(".btn")), t.call(i, "toggle"), e.preventDefault()
    })
}(jQuery), + function($) {
    "use strict";

    function t(t) {
        t && 3 === t.which || ($(n).remove(), $(o).each(function() {
            var i = e($(this)),
                n = {
                    relatedTarget: this
                };
            i.hasClass("open") && (i.trigger(t = $.Event("hide.bs.dropdown", n)), t.isDefaultPrevented() || i.removeClass("open").trigger("hidden.bs.dropdown", n))
        }))
    }

    function e(t) {
        var e = t.attr("data-target");
        e || (e = t.attr("href"), e = e && /#[A-Za-z]/.test(e) && e.replace(/.*(?=#[^\s]*$)/, ""));
        var i = e && $(e);
        return i && i.length ? i : t.parent()
    }

    function i(t) {
        return this.each(function() {
            var e = $(this),
                i = e.data("bs.dropdown");
            i || e.data("bs.dropdown", i = new s(this)), "string" == typeof t && i[t].call(e)
        })
    }
    var n = ".dropdown-backdrop",
        o = '[data-toggle="dropdown"]',
        s = function(t) {
            $(t).on("click.bs.dropdown", this.toggle)
        };
    s.VERSION = "3.2.0", s.prototype.toggle = function(i) {
        var n = $(this);
        if (!n.is(".disabled, :disabled")) {
            var o = e(n),
                s = o.hasClass("open");
            if (t(), !s) {
                "ontouchstart" in document.documentElement && !o.closest(".navbar-nav").length && $('<div class="dropdown-backdrop"/>').insertAfter($(this)).on("click", t);
                var r = {
                    relatedTarget: this
                };
                if (o.trigger(i = $.Event("show.bs.dropdown", r)), i.isDefaultPrevented()) return;
                n.trigger("focus"), o.toggleClass("open").trigger("shown.bs.dropdown", r)
            }
            return !1
        }
    }, s.prototype.keydown = function(t) {
        if (/(38|40|27)/.test(t.keyCode)) {
            var i = $(this);
            if (t.preventDefault(), t.stopPropagation(), !i.is(".disabled, :disabled")) {
                var n = e(i),
                    s = n.hasClass("open");
                if (!s || s && 27 == t.keyCode) return 27 == t.which && n.find(o).trigger("focus"), i.trigger("click");
                var r = " li:not(.divider):visible a",
                    a = n.find('[role="menu"]' + r + ', [role="listbox"]' + r);
                if (a.length) {
                    var l = a.index(a.filter(":focus"));
                    38 == t.keyCode && l > 0 && l--, 40 == t.keyCode && l < a.length - 1 && l++, ~l || (l = 0), a.eq(l).trigger("focus")
                }
            }
        }
    };
    var r = $.fn.dropdown;
    $.fn.dropdown = i, $.fn.dropdown.Constructor = s, $.fn.dropdown.noConflict = function() {
        return $.fn.dropdown = r, this
    }, $(document).on("click.bs.dropdown.data-api", t).on("click.bs.dropdown.data-api", ".dropdown form", function(t) {
        t.stopPropagation()
    }).on("click.bs.dropdown.data-api", o, s.prototype.toggle).on("keydown.bs.dropdown.data-api", o + ', [role="menu"], [role="listbox"]', s.prototype.keydown)
}(jQuery), + function($) {
    "use strict";

    function t(t, i) {
        return this.each(function() {
            var n = $(this),
                o = n.data("bs.modal"),
                s = $.extend({}, e.DEFAULTS, n.data(), "object" == typeof t && t);
            o || n.data("bs.modal", o = new e(this, s)), "string" == typeof t ? o[t](i) : s.show && o.show(i)
        })
    }
    var e = function(t, e) {
        this.options = e, this.$body = $(document.body), this.$element = $(t), this.$backdrop = this.isShown = null, this.scrollbarWidth = 0, this.options.remote && this.$element.find(".modal-content").load(this.options.remote, $.proxy(function() {
            this.$element.trigger("loaded.bs.modal")
        }, this))
    };
    e.VERSION = "3.2.0", e.DEFAULTS = {
        backdrop: !0,
        keyboard: !0,
        show: !0
    }, e.prototype.toggle = function(t) {
        return this.isShown ? this.hide() : this.show(t)
    }, e.prototype.show = function(t) {
        var e = this,
            i = $.Event("show.bs.modal", {
                relatedTarget: t
            });
        this.$element.trigger(i), this.isShown || i.isDefaultPrevented() || (this.isShown = !0, this.checkScrollbar(), this.$body.addClass("modal-open"), this.setScrollbar(), this.escape(), this.$element.on("click.dismiss.bs.modal", '[data-dismiss="modal"]', $.proxy(this.hide, this)), this.backdrop(function() {
            var i = $.support.transition && e.$element.hasClass("fade");
            e.$element.parent().length || e.$element.appendTo(e.$body), e.$element.show().scrollTop(0), i && e.$element[0].offsetWidth, e.$element.addClass("in").attr("aria-hidden", !1), e.enforceFocus();
            var n = $.Event("shown.bs.modal", {
                relatedTarget: t
            });
            i ? e.$element.find(".modal-dialog").one("bsTransitionEnd", function() {
                e.$element.trigger("focus").trigger(n)
            }).emulateTransitionEnd(300) : e.$element.trigger("focus").trigger(n)
        }))
    }, e.prototype.hide = function(t) {
        t && t.preventDefault(), t = $.Event("hide.bs.modal"), this.$element.trigger(t), this.isShown && !t.isDefaultPrevented() && (this.isShown = !1, this.$body.removeClass("modal-open"), this.resetScrollbar(), this.escape(), $(document).off("focusin.bs.modal"), this.$element.removeClass("in").attr("aria-hidden", !0).off("click.dismiss.bs.modal"), $.support.transition && this.$element.hasClass("fade") ? this.$element.one("bsTransitionEnd", $.proxy(this.hideModal, this)).emulateTransitionEnd(300) : this.hideModal())
    }, e.prototype.enforceFocus = function() {
        $(document).off("focusin.bs.modal").on("focusin.bs.modal", $.proxy(function(t) {
            this.$element[0] === t.target || this.$element.has(t.target).length || this.$element.trigger("focus")
        }, this))
    }, e.prototype.escape = function() {
        this.isShown && this.options.keyboard ? this.$element.on("keyup.dismiss.bs.modal", $.proxy(function(t) {
            27 == t.which && this.hide()
        }, this)) : this.isShown || this.$element.off("keyup.dismiss.bs.modal")
    }, e.prototype.hideModal = function() {
        var t = this;
        this.$element.hide(), this.backdrop(function() {
            t.$element.trigger("hidden.bs.modal")
        })
    }, e.prototype.removeBackdrop = function() {
        this.$backdrop && this.$backdrop.remove(), this.$backdrop = null
    }, e.prototype.backdrop = function(t) {
        var e = this,
            i = this.$element.hasClass("fade") ? "fade" : "";
        if (this.isShown && this.options.backdrop) {
            var n = $.support.transition && i;
            if (this.$backdrop = $('<div class="modal-backdrop ' + i + '" />').appendTo(this.$body), this.$element.on("click.dismiss.bs.modal", $.proxy(function(t) {
                    t.target === t.currentTarget && ("static" == this.options.backdrop ? this.$element[0].focus.call(this.$element[0]) : this.hide.call(this))
                }, this)), n && this.$backdrop[0].offsetWidth, this.$backdrop.addClass("in"), !t) return;
            n ? this.$backdrop.one("bsTransitionEnd", t).emulateTransitionEnd(150) : t()
        } else if (!this.isShown && this.$backdrop) {
            this.$backdrop.removeClass("in");
            var o = function() {
                e.removeBackdrop(), t && t()
            };
            $.support.transition && this.$element.hasClass("fade") ? this.$backdrop.one("bsTransitionEnd", o).emulateTransitionEnd(150) : o()
        } else t && t()
    }, e.prototype.checkScrollbar = function() {
        document.body.clientWidth >= window.innerWidth || (this.scrollbarWidth = this.scrollbarWidth || this.measureScrollbar())
    }, e.prototype.setScrollbar = function() {
        var t = parseInt(this.$body.css("padding-right") || 0, 10);
        this.scrollbarWidth && this.$body.css("padding-right", t + this.scrollbarWidth)
    }, e.prototype.resetScrollbar = function() {
        this.$body.css("padding-right", "")
    }, e.prototype.measureScrollbar = function() {
        var t = document.createElement("div");
        t.className = "modal-scrollbar-measure", this.$body.append(t);
        var e = t.offsetWidth - t.clientWidth;
        return this.$body[0].removeChild(t), e
    };
    var i = $.fn.modal;
    $.fn.modal = t, $.fn.modal.Constructor = e, $.fn.modal.noConflict = function() {
        return $.fn.modal = i, this
    }, $(document).on("click.bs.modal.data-api", '[data-toggle="modal"]', function(e) {
        var i = $(this),
            n = i.attr("href"),
            o = $(i.attr("data-target") || n && n.replace(/.*(?=#[^\s]+$)/, "")),
            s = o.data("bs.modal") ? "toggle" : $.extend({
                remote: !/#/.test(n) && n
            }, o.data(), i.data());
        i.is("a") && e.preventDefault(), o.one("show.bs.modal", function(t) {
            t.isDefaultPrevented() || o.one("hidden.bs.modal", function() {
                i.is(":visible") && i.trigger("focus")
            })
        }), t.call(o, s, this)
    })
}(jQuery), + function($) {
    "use strict";

    function t(t) {
        return this.each(function() {
            var i = $(this),
                n = i.data("bs.tooltip"),
                o = "object" == typeof t && t;
            (n || "destroy" != t) && (n || i.data("bs.tooltip", n = new e(this, o)), "string" == typeof t && n[t]())
        })
    }
    var e = function(t, e) {
        this.type = this.options = this.enabled = this.timeout = this.hoverState = this.$element = null, this.init("tooltip", t, e)
    };
    e.VERSION = "3.2.0", e.DEFAULTS = {
        animation: !0,
        placement: "top",
        selector: !1,
        template: '<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',
        trigger: "hover focus",
        title: "",
        delay: 0,
        html: !1,
        container: !1,
        viewport: {
            selector: "body",
            padding: 0
        }
    }, e.prototype.init = function(t, e, i) {
        this.enabled = !0, this.type = t, this.$element = $(e), this.options = this.getOptions(i), this.$viewport = this.options.viewport && $(this.options.viewport.selector || this.options.viewport);
        for (var n = this.options.trigger.split(" "), o = n.length; o--;) {
            var s = n[o];
            if ("click" == s) this.$element.on("click." + this.type, this.options.selector, $.proxy(this.toggle, this));
            else if ("manual" != s) {
                var r = "hover" == s ? "mouseenter" : "focusin",
                    a = "hover" == s ? "mouseleave" : "focusout";
                this.$element.on(r + "." + this.type, this.options.selector, $.proxy(this.enter, this)), this.$element.on(a + "." + this.type, this.options.selector, $.proxy(this.leave, this))
            }
        }
        this.options.selector ? this._options = $.extend({}, this.options, {
            trigger: "manual",
            selector: ""
        }) : this.fixTitle()
    }, e.prototype.getDefaults = function() {
        return e.DEFAULTS
    }, e.prototype.getOptions = function(t) {
        return t = $.extend({}, this.getDefaults(), this.$element.data(), t), t.delay && "number" == typeof t.delay && (t.delay = {
            show: t.delay,
            hide: t.delay
        }), t
    }, e.prototype.getDelegateOptions = function() {
        var t = {},
            e = this.getDefaults();
        return this._options && $.each(this._options, function(i, n) {
            e[i] != n && (t[i] = n)
        }), t
    }, e.prototype.enter = function(t) {
        var e = t instanceof this.constructor ? t : $(t.currentTarget).data("bs." + this.type);
        return e || (e = new this.constructor(t.currentTarget, this.getDelegateOptions()), $(t.currentTarget).data("bs." + this.type, e)), clearTimeout(e.timeout), e.hoverState = "in", e.options.delay && e.options.delay.show ? void(e.timeout = setTimeout(function() {
            "in" == e.hoverState && e.show()
        }, e.options.delay.show)) : e.show()
    }, e.prototype.leave = function(t) {
        var e = t instanceof this.constructor ? t : $(t.currentTarget).data("bs." + this.type);
        return e || (e = new this.constructor(t.currentTarget, this.getDelegateOptions()), $(t.currentTarget).data("bs." + this.type, e)), clearTimeout(e.timeout), e.hoverState = "out", e.options.delay && e.options.delay.hide ? void(e.timeout = setTimeout(function() {
            "out" == e.hoverState && e.hide()
        }, e.options.delay.hide)) : e.hide()
    }, e.prototype.show = function() {
        var t = $.Event("show.bs." + this.type);
        if (this.hasContent() && this.enabled) {
            this.$element.trigger(t);
            var e = $.contains(document.documentElement, this.$element[0]);
            if (t.isDefaultPrevented() || !e) return;
            var i = this,
                n = this.tip(),
                o = this.getUID(this.type);
            this.setContent(), n.attr("id", o), this.$element.attr("aria-describedby", o), this.options.animation && n.addClass("fade");
            var s = "function" == typeof this.options.placement ? this.options.placement.call(this, n[0], this.$element[0]) : this.options.placement,
                r = /\s?auto?\s?/i,
                a = r.test(s);
            a && (s = s.replace(r, "") || "top"), n.detach().css({
                top: 0,
                left: 0,
                display: "block"
            }).addClass(s).data("bs." + this.type, this), this.options.container ? n.appendTo(this.options.container) : n.insertAfter(this.$element);
            var l = this.getPosition(),
                u = n[0].offsetWidth,
                c = n[0].offsetHeight;
            if (a) {
                var h = s,
                    d = this.$element.parent(),
                    p = this.getPosition(d);
                s = "bottom" == s && l.top + l.height + c - p.scroll > p.height ? "top" : "top" == s && l.top - p.scroll - c < 0 ? "bottom" : "right" == s && l.right + u > p.width ? "left" : "left" == s && l.left - u < p.left ? "right" : s, n.removeClass(h).addClass(s)
            }
            var f = this.getCalculatedOffset(s, l, u, c);
            this.applyPlacement(f, s);
            var m = function() {
                i.$element.trigger("shown.bs." + i.type), i.hoverState = null
            };
            $.support.transition && this.$tip.hasClass("fade") ? n.one("bsTransitionEnd", m).emulateTransitionEnd(150) : m()
        }
    }, e.prototype.applyPlacement = function(t, e) {
        var i = this.tip(),
            n = i[0].offsetWidth,
            o = i[0].offsetHeight,
            s = parseInt(i.css("margin-top"), 10),
            r = parseInt(i.css("margin-left"), 10);
        isNaN(s) && (s = 0), isNaN(r) && (r = 0), t.top = t.top + s, t.left = t.left + r, $.offset.setOffset(i[0], $.extend({
            using: function(t) {
                i.css({
                    top: Math.round(t.top),
                    left: Math.round(t.left)
                })
            }
        }, t), 0), i.addClass("in");
        var a = i[0].offsetWidth,
            l = i[0].offsetHeight;
        "top" == e && l != o && (t.top = t.top + o - l);
        var u = this.getViewportAdjustedDelta(e, t, a, l);
        u.left ? t.left += u.left : t.top += u.top;
        var c = u.left ? 2 * u.left - n + a : 2 * u.top - o + l,
            h = u.left ? "left" : "top",
            d = u.left ? "offsetWidth" : "offsetHeight";
        i.offset(t), this.replaceArrow(c, i[0][d], h)
    }, e.prototype.replaceArrow = function(t, e, i) {
        this.arrow().css(i, t ? 50 * (1 - t / e) + "%" : "")
    }, e.prototype.setContent = function() {
        var t = this.tip(),
            e = this.getTitle();
        t.find(".tooltip-inner")[this.options.html ? "html" : "text"](e), t.removeClass("fade in top bottom left right")
    }, e.prototype.hide = function() {
        function t() {
            "in" != e.hoverState && i.detach(), e.$element.trigger("hidden.bs." + e.type)
        }
        var e = this,
            i = this.tip(),
            n = $.Event("hide.bs." + this.type);
        return this.$element.removeAttr("aria-describedby"), this.$element.trigger(n), n.isDefaultPrevented() ? void 0 : (i.removeClass("in"), $.support.transition && this.$tip.hasClass("fade") ? i.one("bsTransitionEnd", t).emulateTransitionEnd(150) : t(), this.hoverState = null, this)
    }, e.prototype.fixTitle = function() {
        var t = this.$element;
        (t.attr("title") || "string" != typeof t.attr("data-original-title")) && t.attr("data-original-title", t.attr("title") || "").attr("title", "")
    }, e.prototype.hasContent = function() {
        return this.getTitle()
    }, e.prototype.getPosition = function(t) {
        t = t || this.$element;
        var e = t[0],
            i = "BODY" == e.tagName;
        return $.extend({}, "function" == typeof e.getBoundingClientRect ? e.getBoundingClientRect() : null, {
            scroll: i ? document.documentElement.scrollTop || document.body.scrollTop : t.scrollTop(),
            width: i ? $(window).width() : t.outerWidth(),
            height: i ? $(window).height() : t.outerHeight()
        }, i ? {
            top: 0,
            left: 0
        } : t.offset())
    }, e.prototype.getCalculatedOffset = function(t, e, i, n) {
        return "bottom" == t ? {
            top: e.top + e.height,
            left: e.left + e.width / 2 - i / 2
        } : "top" == t ? {
            top: e.top - n,
            left: e.left + e.width / 2 - i / 2
        } : "left" == t ? {
            top: e.top + e.height / 2 - n / 2,
            left: e.left - i
        } : {
            top: e.top + e.height / 2 - n / 2,
            left: e.left + e.width
        }
    }, e.prototype.getViewportAdjustedDelta = function(t, e, i, n) {
        var o = {
            top: 0,
            left: 0
        };
        if (!this.$viewport) return o;
        var s = this.options.viewport && this.options.viewport.padding || 0,
            r = this.getPosition(this.$viewport);
        if (/right|left/.test(t)) {
            var a = e.top - s - r.scroll,
                l = e.top + s - r.scroll + n;
            a < r.top ? o.top = r.top - a : l > r.top + r.height && (o.top = r.top + r.height - l)
        } else {
            var u = e.left - s,
                c = e.left + s + i;
            u < r.left ? o.left = r.left - u : c > r.width && (o.left = r.left + r.width - c)
        }
        return o
    }, e.prototype.getTitle = function() {
        var t, e = this.$element,
            i = this.options;
        return t = e.attr("data-original-title") || ("function" == typeof i.title ? i.title.call(e[0]) : i.title)
    }, e.prototype.getUID = function(t) {
        do t += ~~(1e6 * Math.random()); while (document.getElementById(t));
        return t
    }, e.prototype.tip = function() {
        return this.$tip = this.$tip || $(this.options.template)
    }, e.prototype.arrow = function() {
        return this.$arrow = this.$arrow || this.tip().find(".tooltip-arrow")
    }, e.prototype.validate = function() {
        this.$element[0].parentNode || (this.hide(), this.$element = null, this.options = null)
    }, e.prototype.enable = function() {
        this.enabled = !0
    }, e.prototype.disable = function() {
        this.enabled = !1
    }, e.prototype.toggleEnabled = function() {
        this.enabled = !this.enabled
    }, e.prototype.toggle = function(t) {
        var e = this;
        t && (e = $(t.currentTarget).data("bs." + this.type), e || (e = new this.constructor(t.currentTarget, this.getDelegateOptions()), $(t.currentTarget).data("bs." + this.type, e))), e.tip().hasClass("in") ? e.leave(e) : e.enter(e)
    }, e.prototype.destroy = function() {
        clearTimeout(this.timeout), this.hide().$element.off("." + this.type).removeData("bs." + this.type)
    };
    var i = $.fn.tooltip;
    $.fn.tooltip = t, $.fn.tooltip.Constructor = e, $.fn.tooltip.noConflict = function() {
        return $.fn.tooltip = i, this
    }
}(jQuery), + function($) {
    "use strict";

    function t(t) {
        return this.each(function() {
            var i = $(this),
                n = i.data("bs.tab");
            n || i.data("bs.tab", n = new e(this)), "string" == typeof t && n[t]()
        })
    }
    var e = function(t) {
        this.element = $(t)
    };
    e.VERSION = "3.2.0", e.prototype.show = function() {
        var t = this.element,
            e = t.closest("ul:not(.dropdown-menu)"),
            i = t.data("target");
        if (i || (i = t.attr("href"), i = i && i.replace(/.*(?=#[^\s]*$)/, "")), !t.parent("li").hasClass("active")) {
            var n = e.find(".active:last a")[0],
                o = $.Event("show.bs.tab", {
                    relatedTarget: n
                });
            if (t.trigger(o), !o.isDefaultPrevented()) {
                var s = $(i);
                this.activate(t.closest("li"), e), this.activate(s, s.parent(), function() {
                    t.trigger({
                        type: "shown.bs.tab",
                        relatedTarget: n
                    })
                })
            }
        }
    }, e.prototype.activate = function(t, e, i) {
        function n() {
            o.removeClass("active").find("> .dropdown-menu > .active").removeClass("active"), t.addClass("active"), s ? (t[0].offsetWidth, t.addClass("in")) : t.removeClass("fade"), t.parent(".dropdown-menu") && t.closest("li.dropdown").addClass("active"), i && i()
        }
        var o = e.find("> .active"),
            s = i && $.support.transition && o.hasClass("fade");
        s ? o.one("bsTransitionEnd", n).emulateTransitionEnd(150) : n(), o.removeClass("in")
    };
    var i = $.fn.tab;
    $.fn.tab = t, $.fn.tab.Constructor = e, $.fn.tab.noConflict = function() {
        return $.fn.tab = i, this
    }, $(document).on("click.bs.tab.data-api", '[data-toggle="tab"], [data-toggle="pill"]', function(e) {
        e.preventDefault(), t.call($(this), "show")
    })
}(jQuery), + function($) {
    "use strict";

    function t(t) {
        return this.each(function() {
            var i = $(this),
                n = i.data("bs.collapse"),
                o = $.extend({}, e.DEFAULTS, i.data(), "object" == typeof t && t);
            !n && o.toggle && "show" == t && (t = !t), n || i.data("bs.collapse", n = new e(this, o)), "string" == typeof t && n[t]()
        })
    }
    var e = function(t, i) {
        this.$element = $(t), this.options = $.extend({}, e.DEFAULTS, i), this.transitioning = null, this.options.parent && (this.$parent = $(this.options.parent)), this.options.toggle && this.toggle()
    };
    e.VERSION = "3.2.0", e.DEFAULTS = {
        toggle: !0
    }, e.prototype.dimension = function() {
        var t = this.$element.hasClass("width");
        return t ? "width" : "height"
    }, e.prototype.show = function() {
        if (!this.transitioning && !this.$element.hasClass("in")) {
            var e = $.Event("show.bs.collapse");
            if (this.$element.trigger(e), !e.isDefaultPrevented()) {
                var i = this.$parent && this.$parent.find("> .panel > .in");
                if (i && i.length) {
                    var n = i.data("bs.collapse");
                    if (n && n.transitioning) return;
                    t.call(i, "hide"), n || i.data("bs.collapse", null)
                }
                var o = this.dimension();
                this.$element.removeClass("collapse").addClass("collapsing")[o](0), this.transitioning = 1;
                var s = function() {
                    this.$element.removeClass("collapsing").addClass("collapse in")[o](""), this.transitioning = 0, this.$element.trigger("shown.bs.collapse")
                };
                if (!$.support.transition) return s.call(this);
                var r = $.camelCase(["scroll", o].join("-"));
                this.$element.one("bsTransitionEnd", $.proxy(s, this)).emulateTransitionEnd(350)[o](this.$element[0][r])
            }
        }
    }, e.prototype.hide = function() {
        if (!this.transitioning && this.$element.hasClass("in")) {
            var t = $.Event("hide.bs.collapse");
            if (this.$element.trigger(t), !t.isDefaultPrevented()) {
                var e = this.dimension();
                this.$element[e](this.$element[e]())[0].offsetHeight, this.$element.addClass("collapsing").removeClass("collapse").removeClass("in"), this.transitioning = 1;
                var i = function() {
                    this.transitioning = 0, this.$element.trigger("hidden.bs.collapse").removeClass("collapsing").addClass("collapse")
                };
                return $.support.transition ? void this.$element[e](0).one("bsTransitionEnd", $.proxy(i, this)).emulateTransitionEnd(350) : i.call(this)
            }
        }
    }, e.prototype.toggle = function() {
        this[this.$element.hasClass("in") ? "hide" : "show"]()
    };
    var i = $.fn.collapse;
    $.fn.collapse = t, $.fn.collapse.Constructor = e, $.fn.collapse.noConflict = function() {
        return $.fn.collapse = i, this
    }, $(document).on("click.bs.collapse.data-api", '[data-toggle="collapse"]', function(e) {
        var i, n = $(this),
            o = n.attr("data-target") || e.preventDefault() || (i = n.attr("href")) && i.replace(/.*(?=#[^\s]+$)/, ""),
            s = $(o),
            r = s.data("bs.collapse"),
            a = r ? "toggle" : n.data(),
            l = n.attr("data-parent"),
            u = l && $(l);
        r && r.transitioning || (u && u.find('[data-toggle="collapse"][data-parent="' + l + '"]').not(n).addClass("collapsed"), n[s.hasClass("in") ? "addClass" : "removeClass"]("collapsed")), t.call(s, a)
    })
}(jQuery), + function($) {
    "use strict";

    function t() {
        var t = document.createElement("bootstrap"),
            e = {
                WebkitTransition: "webkitTransitionEnd",
                MozTransition: "transitionend",
                OTransition: "oTransitionEnd otransitionend",
                transition: "transitionend"
            };
        for (var i in e)
            if (void 0 !== t.style[i]) return {
                end: e[i]
            };
        return !1
    }
    $.fn.emulateTransitionEnd = function(t) {
        var e = !1,
            i = this;
        $(this).one("bsTransitionEnd", function() {
            e = !0
        });
        var n = function() {
            e || $(i).trigger($.support.transition.end)
        };
        return setTimeout(n, t), this
    }, $(function() {
        $.support.transition = t(), $.support.transition && ($.event.special.bsTransitionEnd = {
            bindType: $.support.transition.end,
            delegateType: $.support.transition.end,
            handle: function(t) {
                return $(t.target).is(this) ? t.handleObj.handler.apply(this, arguments) : void 0
            }
        })
    })
}(jQuery),
function($) {
    $.flexslider = function(t, e) {
        var i = $(t);
        i.vars = $.extend({}, $.flexslider.defaults, e);
        var n = i.vars.namespace,
            o = window.navigator && window.navigator.msPointerEnabled && window.MSGesture,
            s = ("ontouchstart" in window || o || window.DocumentTouch && document instanceof DocumentTouch) && i.vars.touch,
            r = "click touchend MSPointerUp keyup",
            a = "",
            l, u = "vertical" === i.vars.direction,
            c = i.vars.reverse,
            h = i.vars.itemWidth > 0,
            d = "fade" === i.vars.animation,
            p = "" !== i.vars.asNavFor,
            f = {},
            m = !0;
        $.data(t, "flexslider", i), f = {
            init: function() {
                i.animating = !1, i.currentSlide = parseInt(i.vars.startAt ? i.vars.startAt : 0, 10), isNaN(i.currentSlide) && (i.currentSlide = 0), i.animatingTo = i.currentSlide, i.atEnd = 0 === i.currentSlide || i.currentSlide === i.last, i.containerSelector = i.vars.selector.substr(0, i.vars.selector.search(" ")), i.slides = $(i.vars.selector, i), i.container = $(i.containerSelector, i), i.count = i.slides.length, i.syncExists = $(i.vars.sync).length > 0, "slide" === i.vars.animation && (i.vars.animation = "swing"), i.prop = u ? "top" : "marginLeft", i.args = {}, i.manualPause = !1, i.stopped = !1, i.started = !1,
                    i.startTimeout = null, i.transitions = !i.vars.video && !d && i.vars.useCSS && function() {
                        var t = document.createElement("div"),
                            e = ["perspectiveProperty", "WebkitPerspective", "MozPerspective", "OPerspective", "msPerspective"];
                        for (var n in e)
                            if (void 0 !== t.style[e[n]]) return i.pfx = e[n].replace("Perspective", "").toLowerCase(), i.prop = "-" + i.pfx + "-transform", !0;
                        return !1
                    }(), i.ensureAnimationEnd = "", "" !== i.vars.controlsContainer && (i.controlsContainer = $(i.vars.controlsContainer).length > 0 && $(i.vars.controlsContainer)), "" !== i.vars.manualControls && (i.manualControls = $(i.vars.manualControls).length > 0 && $(i.vars.manualControls)), i.vars.randomize && (i.slides.sort(function() {
                        return Math.round(Math.random()) - .5
                    }), i.container.empty().append(i.slides)), i.doMath(), i.setup("init"), i.vars.controlNav && f.controlNav.setup(), i.vars.directionNav && f.directionNav.setup(), i.vars.keyboard && (1 === $(i.containerSelector).length || i.vars.multipleKeyboard) && $(document).bind("keyup", function(t) {
                        var e = t.keyCode;
                        if (!i.animating && (39 === e || 37 === e)) {
                            var n = 39 === e ? i.getTarget("next") : 37 === e ? i.getTarget("prev") : !1;
                            i.flexAnimate(n, i.vars.pauseOnAction)
                        }
                    }), i.vars.mousewheel && i.bind("mousewheel", function(t, e, n, o) {
                        t.preventDefault();
                        var s = 0 > e ? i.getTarget("next") : i.getTarget("prev");
                        i.flexAnimate(s, i.vars.pauseOnAction)
                    }), i.vars.pausePlay && f.pausePlay.setup(), i.vars.slideshow && i.vars.pauseInvisible && f.pauseInvisible.init(), i.vars.slideshow && (i.vars.pauseOnHover && i.hover(function() {
                        i.manualPlay || i.manualPause || i.pause()
                    }, function() {
                        i.manualPause || i.manualPlay || i.stopped || i.play()
                    }), i.vars.pauseInvisible && f.pauseInvisible.isHidden() || (i.vars.initDelay > 0 ? i.startTimeout = setTimeout(i.play, i.vars.initDelay) : i.play())), p && f.asNav.setup(), s && i.vars.touch && f.touch(), (!d || d && i.vars.smoothHeight) && $(window).bind("resize orientationchange focus", f.resize), i.find("img").attr("draggable", "false"), setTimeout(function() {
                        i.vars.start(i)
                    }, 200)
            },
            asNav: {
                setup: function() {
                    i.asNav = !0, i.animatingTo = Math.floor(i.currentSlide / i.move), i.currentItem = i.currentSlide, i.slides.removeClass(n + "active-slide").eq(i.currentItem).addClass(n + "active-slide"), o ? (t._slider = i, i.slides.each(function() {
                        var t = this;
                        t._gesture = new MSGesture, t._gesture.target = t, t.addEventListener("MSPointerDown", function(t) {
                            t.preventDefault(), t.currentTarget._gesture && t.currentTarget._gesture.addPointer(t.pointerId)
                        }, !1), t.addEventListener("MSGestureTap", function(t) {
                            t.preventDefault();
                            var e = $(this),
                                n = e.index();
                            $(i.vars.asNavFor).data("flexslider").animating || e.hasClass("active") || (i.direction = i.currentItem < n ? "next" : "prev", i.flexAnimate(n, i.vars.pauseOnAction, !1, !0, !0))
                        })
                    })) : i.slides.on(r, function(t) {
                        t.preventDefault();
                        var e = $(this),
                            o = e.index(),
                            s = e.offset().left - $(i).scrollLeft();
                        0 >= s && e.hasClass(n + "active-slide") ? i.flexAnimate(i.getTarget("prev"), !0) : $(i.vars.asNavFor).data("flexslider").animating || e.hasClass(n + "active-slide") || (i.direction = i.currentItem < o ? "next" : "prev", i.flexAnimate(o, i.vars.pauseOnAction, !1, !0, !0))
                    })
                }
            },
            controlNav: {
                setup: function() {
                    i.manualControls ? f.controlNav.setupManual() : f.controlNav.setupPaging()
                },
                setupPaging: function() {
                    var t = "thumbnails" === i.vars.controlNav ? "control-thumbs" : "control-paging",
                        e = 1,
                        o, s;
                    if (i.controlNavScaffold = $('<ol class="' + n + "control-nav " + n + t + '"></ol>'), i.pagingCount > 1)
                        for (var l = 0; l < i.pagingCount; l++) {
                            if (s = i.slides.eq(l), o = "thumbnails" === i.vars.controlNav ? '<img src="' + s.attr("data-thumb") + '"/>' : "<a>" + e + "</a>", "thumbnails" === i.vars.controlNav && !0 === i.vars.thumbCaptions) {
                                var u = s.attr("data-thumbcaption");
                                "" != u && void 0 != u && (o += '<span class="' + n + 'caption">' + u + "</span>")
                            }
                            i.controlNavScaffold.append("<li>" + o + "</li>"), e++
                        }
                    i.controlsContainer ? $(i.controlsContainer).append(i.controlNavScaffold) : i.append(i.controlNavScaffold), f.controlNav.set(), f.controlNav.active(), i.controlNavScaffold.delegate("a, img", r, function(t) {
                        if (t.preventDefault(), "" === a || a === t.type) {
                            var e = $(this),
                                o = i.controlNav.index(e);
                            e.hasClass(n + "active") || (i.direction = o > i.currentSlide ? "next" : "prev", i.flexAnimate(o, i.vars.pauseOnAction))
                        }
                        "" === a && (a = t.type), f.setToClearWatchedEvent()
                    })
                },
                setupManual: function() {
                    i.controlNav = i.manualControls, f.controlNav.active(), i.controlNav.bind(r, function(t) {
                        if (t.preventDefault(), "" === a || a === t.type) {
                            var e = $(this),
                                o = i.controlNav.index(e);
                            e.hasClass(n + "active") || (o > i.currentSlide ? i.direction = "next" : i.direction = "prev", i.flexAnimate(o, i.vars.pauseOnAction))
                        }
                        "" === a && (a = t.type), f.setToClearWatchedEvent()
                    })
                },
                set: function() {
                    var t = "thumbnails" === i.vars.controlNav ? "img" : "a";
                    i.controlNav = $("." + n + "control-nav li " + t, i.controlsContainer ? i.controlsContainer : i)
                },
                active: function() {
                    i.controlNav.removeClass(n + "active").eq(i.animatingTo).addClass(n + "active")
                },
                update: function(t, e) {
                    i.pagingCount > 1 && "add" === t ? i.controlNavScaffold.append($("<li><a>" + i.count + "</a></li>")) : 1 === i.pagingCount ? i.controlNavScaffold.find("li").remove() : i.controlNav.eq(e).closest("li").remove(), f.controlNav.set(), i.pagingCount > 1 && i.pagingCount !== i.controlNav.length ? i.update(e, t) : f.controlNav.active()
                }
            },
            directionNav: {
                setup: function() {
                    var t = $('<ul class="' + n + 'direction-nav"><li><a class="' + n + 'prev" href="#">' + i.vars.prevText + '</a></li><li><a class="' + n + 'next" href="#">' + i.vars.nextText + "</a></li></ul>");
                    i.controlsContainer ? ($(i.controlsContainer).append(t), i.directionNav = $("." + n + "direction-nav li a", i.controlsContainer)) : (i.append(t), i.directionNav = $("." + n + "direction-nav li a", i)), f.directionNav.update(), i.directionNav.bind(r, function(t) {
                        t.preventDefault();
                        var e;
                        ("" === a || a === t.type) && (e = $(this).hasClass(n + "next") ? i.getTarget("next") : i.getTarget("prev"), i.flexAnimate(e, i.vars.pauseOnAction)), "" === a && (a = t.type), f.setToClearWatchedEvent()
                    })
                },
                update: function() {
                    var t = n + "disabled";
                    1 === i.pagingCount ? i.directionNav.addClass(t).attr("tabindex", "-1") : i.vars.animationLoop ? i.directionNav.removeClass(t).removeAttr("tabindex") : 0 === i.animatingTo ? i.directionNav.removeClass(t).filter("." + n + "prev").addClass(t).attr("tabindex", "-1") : i.animatingTo === i.last ? i.directionNav.removeClass(t).filter("." + n + "next").addClass(t).attr("tabindex", "-1") : i.directionNav.removeClass(t).removeAttr("tabindex")
                }
            },
            pausePlay: {
                setup: function() {
                    var t = $('<div class="' + n + 'pauseplay"><a></a></div>');
                    i.controlsContainer ? (i.controlsContainer.append(t), i.pausePlay = $("." + n + "pauseplay a", i.controlsContainer)) : (i.append(t), i.pausePlay = $("." + n + "pauseplay a", i)), f.pausePlay.update(i.vars.slideshow ? n + "pause" : n + "play"), i.pausePlay.bind(r, function(t) {
                        t.preventDefault(), ("" === a || a === t.type) && ($(this).hasClass(n + "pause") ? (i.manualPause = !0, i.manualPlay = !1, i.pause()) : (i.manualPause = !1, i.manualPlay = !0, i.play())), "" === a && (a = t.type), f.setToClearWatchedEvent()
                    })
                },
                update: function(t) {
                    "play" === t ? i.pausePlay.removeClass(n + "pause").addClass(n + "play").html(i.vars.playText) : i.pausePlay.removeClass(n + "play").addClass(n + "pause").html(i.vars.pauseText)
                }
            },
            touch: function() {
                function e(e) {
                    i.animating ? e.preventDefault() : (window.navigator.msPointerEnabled || 1 === e.touches.length) && (i.pause(), v = u ? i.h : i.w, y = Number(new Date), w = e.touches[0].pageX, S = e.touches[0].pageY, m = h && c && i.animatingTo === i.last ? 0 : h && c ? i.limit - (i.itemW + i.vars.itemMargin) * i.move * i.animatingTo : h && i.currentSlide === i.last ? i.limit : h ? (i.itemW + i.vars.itemMargin) * i.move * i.currentSlide : c ? (i.last - i.currentSlide + i.cloneOffset) * v : (i.currentSlide + i.cloneOffset) * v, p = u ? S : w, f = u ? w : S, t.addEventListener("touchmove", n, !1), t.addEventListener("touchend", s, !1))
                }

                function n(t) {
                    w = t.touches[0].pageX, S = t.touches[0].pageY, g = u ? p - S : p - w, b = u ? Math.abs(g) < Math.abs(w - f) : Math.abs(g) < Math.abs(S - f);
                    var e = 500;
                    (!b || Number(new Date) - y > e) && (t.preventDefault(), !d && i.transitions && (i.vars.animationLoop || (g /= 0 === i.currentSlide && 0 > g || i.currentSlide === i.last && g > 0 ? Math.abs(g) / v + 2 : 1), i.setProps(m + g, "setTouch")))
                }

                function s(e) {
                    if (t.removeEventListener("touchmove", n, !1), i.animatingTo === i.currentSlide && !b && null !== g) {
                        var o = c ? -g : g,
                            r = o > 0 ? i.getTarget("next") : i.getTarget("prev");
                        i.canAdvance(r) && (Number(new Date) - y < 550 && Math.abs(o) > 50 || Math.abs(o) > v / 2) ? i.flexAnimate(r, i.vars.pauseOnAction) : d || i.flexAnimate(i.currentSlide, i.vars.pauseOnAction, !0)
                    }
                    t.removeEventListener("touchend", s, !1), p = null, f = null, g = null, m = null
                }

                function r(e) {
                    e.stopPropagation(), i.animating ? e.preventDefault() : (i.pause(), t._gesture.addPointer(e.pointerId), C = 0, v = u ? i.h : i.w, y = Number(new Date), m = h && c && i.animatingTo === i.last ? 0 : h && c ? i.limit - (i.itemW + i.vars.itemMargin) * i.move * i.animatingTo : h && i.currentSlide === i.last ? i.limit : h ? (i.itemW + i.vars.itemMargin) * i.move * i.currentSlide : c ? (i.last - i.currentSlide + i.cloneOffset) * v : (i.currentSlide + i.cloneOffset) * v)
                }

                function a(e) {
                    e.stopPropagation();
                    var i = e.target._slider;
                    if (i) {
                        var n = -e.translationX,
                            o = -e.translationY;
                        return C += u ? o : n, g = C, b = u ? Math.abs(C) < Math.abs(-n) : Math.abs(C) < Math.abs(-o), e.detail === e.MSGESTURE_FLAG_INERTIA ? void setImmediate(function() {
                            t._gesture.stop()
                        }) : void((!b || Number(new Date) - y > 500) && (e.preventDefault(), !d && i.transitions && (i.vars.animationLoop || (g = C / (0 === i.currentSlide && 0 > C || i.currentSlide === i.last && C > 0 ? Math.abs(C) / v + 2 : 1)), i.setProps(m + g, "setTouch"))))
                    }
                }

                function l(t) {
                    t.stopPropagation();
                    var e = t.target._slider;
                    if (e) {
                        if (e.animatingTo === e.currentSlide && !b && null !== g) {
                            var i = c ? -g : g,
                                n = i > 0 ? e.getTarget("next") : e.getTarget("prev");
                            e.canAdvance(n) && (Number(new Date) - y < 550 && Math.abs(i) > 50 || Math.abs(i) > v / 2) ? e.flexAnimate(n, e.vars.pauseOnAction) : d || e.flexAnimate(e.currentSlide, e.vars.pauseOnAction, !0)
                        }
                        p = null, f = null, g = null, m = null, C = 0
                    }
                }
                var p, f, m, v, g, y, b = !1,
                    w = 0,
                    S = 0,
                    C = 0;
                o ? (t.style.msTouchAction = "none", t._gesture = new MSGesture, t._gesture.target = t, t.addEventListener("MSPointerDown", r, !1), t._slider = i, t.addEventListener("MSGestureChange", a, !1), t.addEventListener("MSGestureEnd", l, !1)) : t.addEventListener("touchstart", e, !1)
            },
            resize: function() {
                !i.animating && i.is(":visible") && (h || i.doMath(), d ? f.smoothHeight() : h ? (i.slides.width(i.computedW), i.update(i.pagingCount), i.setProps()) : u ? (i.viewport.height(i.h), i.setProps(i.h, "setTotal")) : (i.vars.smoothHeight && f.smoothHeight(), i.newSlides.width(i.computedW), i.setProps(i.computedW, "setTotal")))
            },
            smoothHeight: function(t) {
                if (!u || d) {
                    var e = d ? i : i.viewport;
                    t ? e.animate({
                        height: i.slides.eq(i.animatingTo).height()
                    }, t) : e.height(i.slides.eq(i.animatingTo).height())
                }
            },
            sync: function(t) {
                var e = $(i.vars.sync).data("flexslider"),
                    n = i.animatingTo;
                switch (t) {
                    case "animate":
                        e.flexAnimate(n, i.vars.pauseOnAction, !1, !0);
                        break;
                    case "play":
                        e.playing || e.asNav || e.play();
                        break;
                    case "pause":
                        e.pause()
                }
            },
            uniqueID: function(t) {
                return t.filter("[id]").add(t.find("[id]")).each(function() {
                    var t = $(this);
                    t.attr("id", t.attr("id") + "_clone")
                }), t
            },
            pauseInvisible: {
                visProp: null,
                init: function() {
                    var t = ["webkit", "moz", "ms", "o"];
                    if ("hidden" in document) return "hidden";
                    for (var e = 0; e < t.length; e++) t[e] + "Hidden" in document && (f.pauseInvisible.visProp = t[e] + "Hidden");
                    if (f.pauseInvisible.visProp) {
                        var n = f.pauseInvisible.visProp.replace(/[H|h]idden/, "") + "visibilitychange";
                        document.addEventListener(n, function() {
                            f.pauseInvisible.isHidden() ? i.startTimeout ? clearTimeout(i.startTimeout) : i.pause() : i.started ? i.play() : i.vars.initDelay > 0 ? setTimeout(i.play, i.vars.initDelay) : i.play()
                        })
                    }
                },
                isHidden: function() {
                    return document[f.pauseInvisible.visProp] || !1
                }
            },
            setToClearWatchedEvent: function() {
                clearTimeout(l), l = setTimeout(function() {
                    a = ""
                }, 3e3)
            }
        }, i.flexAnimate = function(t, e, o, r, a) {
            if (i.vars.animationLoop || t === i.currentSlide || (i.direction = t > i.currentSlide ? "next" : "prev"), p && 1 === i.pagingCount && (i.direction = i.currentItem < t ? "next" : "prev"), !i.animating && (i.canAdvance(t, a) || o) && i.is(":visible")) {
                if (p && r) {
                    var l = $(i.vars.asNavFor).data("flexslider");
                    if (i.atEnd = 0 === t || t === i.count - 1, l.flexAnimate(t, !0, !1, !0, a), i.direction = i.currentItem < t ? "next" : "prev", l.direction = i.direction, Math.ceil((t + 1) / i.visible) - 1 === i.currentSlide || 0 === t) return i.currentItem = t, i.slides.removeClass(n + "active-slide").eq(t).addClass(n + "active-slide"), !1;
                    i.currentItem = t, i.slides.removeClass(n + "active-slide").eq(t).addClass(n + "active-slide"), t = Math.floor(t / i.visible)
                }
                if (i.animating = !0, i.animatingTo = t, e && i.pause(), i.vars.before(i), i.syncExists && !a && f.sync("animate"), i.vars.controlNav && f.controlNav.active(), h || i.slides.removeClass(n + "active-slide").eq(t).addClass(n + "active-slide"), i.atEnd = 0 === t || t === i.last, i.vars.directionNav && f.directionNav.update(), t === i.last && (i.vars.end(i), i.vars.animationLoop || i.pause()), d) s ? (i.slides.eq(i.currentSlide).css({
                    opacity: 0,
                    zIndex: 1
                }), i.slides.eq(t).css({
                    opacity: 1,
                    zIndex: 2
                }), i.wrapup(m)) : (i.slides.eq(i.currentSlide).css({
                    zIndex: 1
                }).animate({
                    opacity: 0
                }, i.vars.animationSpeed, i.vars.easing), i.slides.eq(t).css({
                    zIndex: 2
                }).animate({
                    opacity: 1
                }, i.vars.animationSpeed, i.vars.easing, i.wrapup));
                else {
                    var m = u ? i.slides.filter(":first").height() : i.computedW,
                        v, g, y;
                    h ? (v = i.vars.itemMargin, y = (i.itemW + v) * i.move * i.animatingTo, g = y > i.limit && 1 !== i.visible ? i.limit : y) : g = 0 === i.currentSlide && t === i.count - 1 && i.vars.animationLoop && "next" !== i.direction ? c ? (i.count + i.cloneOffset) * m : 0 : i.currentSlide === i.last && 0 === t && i.vars.animationLoop && "prev" !== i.direction ? c ? 0 : (i.count + 1) * m : c ? (i.count - 1 - t + i.cloneOffset) * m : (t + i.cloneOffset) * m, i.setProps(g, "", i.vars.animationSpeed), i.transitions ? (i.vars.animationLoop && i.atEnd || (i.animating = !1, i.currentSlide = i.animatingTo), i.container.unbind("webkitTransitionEnd transitionend"), i.container.bind("webkitTransitionEnd transitionend", function() {
                        clearTimeout(i.ensureAnimationEnd), i.wrapup(m)
                    }), clearTimeout(i.ensureAnimationEnd), i.ensureAnimationEnd = setTimeout(function() {
                        i.wrapup(m)
                    }, i.vars.animationSpeed + 100)) : i.container.animate(i.args, i.vars.animationSpeed, i.vars.easing, function() {
                        i.wrapup(m)
                    })
                }
                i.vars.smoothHeight && f.smoothHeight(i.vars.animationSpeed)
            }
        }, i.wrapup = function(t) {
            d || h || (0 === i.currentSlide && i.animatingTo === i.last && i.vars.animationLoop ? i.setProps(t, "jumpEnd") : i.currentSlide === i.last && 0 === i.animatingTo && i.vars.animationLoop && i.setProps(t, "jumpStart")), i.animating = !1, i.currentSlide = i.animatingTo, i.vars.after(i)
        }, i.animateSlides = function() {
            !i.animating && m && i.flexAnimate(i.getTarget("next"))
        }, i.pause = function() {
            clearInterval(i.animatedSlides), i.animatedSlides = null, i.playing = !1, i.vars.pausePlay && f.pausePlay.update("play"), i.syncExists && f.sync("pause")
        }, i.play = function() {
            i.playing && clearInterval(i.animatedSlides), i.animatedSlides = i.animatedSlides || setInterval(i.animateSlides, i.vars.slideshowSpeed), i.started = i.playing = !0, i.vars.pausePlay && f.pausePlay.update("pause"), i.syncExists && f.sync("play")
        }, i.stop = function() {
            i.pause(), i.stopped = !0
        }, i.canAdvance = function(t, e) {
            var n = p ? i.pagingCount - 1 : i.last;
            return e ? !0 : p && i.currentItem === i.count - 1 && 0 === t && "prev" === i.direction ? !0 : p && 0 === i.currentItem && t === i.pagingCount - 1 && "next" !== i.direction ? !1 : t !== i.currentSlide || p ? i.vars.animationLoop ? !0 : i.atEnd && 0 === i.currentSlide && t === n && "next" !== i.direction ? !1 : i.atEnd && i.currentSlide === n && 0 === t && "next" === i.direction ? !1 : !0 : !1
        }, i.getTarget = function(t) {
            return i.direction = t, "next" === t ? i.currentSlide === i.last ? 0 : i.currentSlide + 1 : 0 === i.currentSlide ? i.last : i.currentSlide - 1
        }, i.setProps = function(t, e, n) {
            var o = function() {
                var n = t ? t : (i.itemW + i.vars.itemMargin) * i.move * i.animatingTo,
                    o = function() {
                        if (h) return "setTouch" === e ? t : c && i.animatingTo === i.last ? 0 : c ? i.limit - (i.itemW + i.vars.itemMargin) * i.move * i.animatingTo : i.animatingTo === i.last ? i.limit : n;
                        switch (e) {
                            case "setTotal":
                                return c ? (i.count - 1 - i.currentSlide + i.cloneOffset) * t : (i.currentSlide + i.cloneOffset) * t;
                            case "setTouch":
                                return c ? t : t;
                            case "jumpEnd":
                                return c ? t : i.count * t;
                            case "jumpStart":
                                return c ? i.count * t : t;
                            default:
                                return t
                        }
                    }();
                return -1 * o + "px"
            }();
            i.transitions && (o = u ? "translate3d(0," + o + ",0)" : "translate3d(" + o + ",0,0)", n = void 0 !== n ? n / 1e3 + "s" : "0s", i.container.css("-" + i.pfx + "-transition-duration", n), i.container.css("transition-duration", n)), i.args[i.prop] = o, (i.transitions || void 0 === n) && i.container.css(i.args), i.container.css("transform", o)
        }, i.setup = function(t) {
            if (d) i.slides.css({
                width: "100%",
                "float": "left",
                marginRight: "-100%",
                position: "relative"
            }), "init" === t && (s ? i.slides.css({
                opacity: 0,
                display: "block",
                webkitTransition: "opacity " + i.vars.animationSpeed / 1e3 + "s ease",
                zIndex: 1
            }).eq(i.currentSlide).css({
                opacity: 1,
                zIndex: 2
            }) : 0 == i.vars.fadeFirstSlide ? i.slides.css({
                opacity: 0,
                display: "block",
                zIndex: 1
            }).eq(i.currentSlide).css({
                zIndex: 2
            }).css({
                opacity: 1
            }) : i.slides.css({
                opacity: 0,
                display: "block",
                zIndex: 1
            }).eq(i.currentSlide).css({
                zIndex: 2
            }).animate({
                opacity: 1
            }, i.vars.animationSpeed, i.vars.easing)), i.vars.smoothHeight && f.smoothHeight();
            else {
                var e, o;
                "init" === t && (i.viewport = $('<div class="' + n + 'viewport"></div>').css({
                    overflow: "hidden",
                    position: "relative"
                }).appendTo(i).append(i.container), i.cloneCount = 0, i.cloneOffset = 0, c && (o = $.makeArray(i.slides).reverse(), i.slides = $(o), i.container.empty().append(i.slides))), i.vars.animationLoop && !h && (i.cloneCount = 2, i.cloneOffset = 1, "init" !== t && i.container.find(".clone").remove(), i.container.append(f.uniqueID(i.slides.first().clone().addClass("clone")).attr("aria-hidden", "true")).prepend(f.uniqueID(i.slides.last().clone().addClass("clone")).attr("aria-hidden", "true"))), i.newSlides = $(i.vars.selector, i), e = c ? i.count - 1 - i.currentSlide + i.cloneOffset : i.currentSlide + i.cloneOffset, u && !h ? (i.container.height(200 * (i.count + i.cloneCount) + "%").css("position", "absolute").width("100%"), setTimeout(function() {
                    i.newSlides.css({
                        display: "block"
                    }), i.doMath(), i.viewport.height(i.h), i.setProps(e * i.h, "init")
                }, "init" === t ? 100 : 0)) : (i.container.width(200 * (i.count + i.cloneCount) + "%"), i.setProps(e * i.computedW, "init"), setTimeout(function() {
                    i.doMath(), i.newSlides.css({
                        width: i.computedW,
                        "float": "left",
                        display: "block"
                    }), i.vars.smoothHeight && f.smoothHeight()
                }, "init" === t ? 100 : 0))
            }
            h || i.slides.removeClass(n + "active-slide").eq(i.currentSlide).addClass(n + "active-slide"), i.vars.init(i)
        }, i.doMath = function() {
            var t = i.slides.first(),
                e = i.vars.itemMargin,
                n = i.vars.minItems,
                o = i.vars.maxItems;
            i.w = void 0 === i.viewport ? i.width() : i.viewport.width(), i.h = t.height(), i.boxPadding = t.outerWidth() - t.width(), h ? (i.itemT = i.vars.itemWidth + e, i.minW = n ? n * i.itemT : i.w, i.maxW = o ? o * i.itemT - e : i.w, i.itemW = i.minW > i.w ? (i.w - e * (n - 1)) / n : i.maxW < i.w ? (i.w - e * (o - 1)) / o : i.vars.itemWidth > i.w ? i.w : i.vars.itemWidth, i.visible = Math.floor(i.w / i.itemW), i.move = i.vars.move > 0 && i.vars.move < i.visible ? i.vars.move : i.visible, i.pagingCount = Math.ceil((i.count - i.visible) / i.move + 1), i.last = i.pagingCount - 1, i.limit = 1 === i.pagingCount ? 0 : i.vars.itemWidth > i.w ? i.itemW * (i.count - 1) + e * (i.count - 1) : (i.itemW + e) * i.count - i.w - e) : (i.itemW = i.w, i.pagingCount = i.count, i.last = i.count - 1), i.computedW = i.itemW - i.boxPadding
        }, i.update = function(t, e) {
            i.doMath(), h || (t < i.currentSlide ? i.currentSlide += 1 : t <= i.currentSlide && 0 !== t && (i.currentSlide -= 1), i.animatingTo = i.currentSlide), i.vars.controlNav && !i.manualControls && ("add" === e && !h || i.pagingCount > i.controlNav.length ? f.controlNav.update("add") : ("remove" === e && !h || i.pagingCount < i.controlNav.length) && (h && i.currentSlide > i.last && (i.currentSlide -= 1, i.animatingTo -= 1), f.controlNav.update("remove", i.last))), i.vars.directionNav && f.directionNav.update()
        }, i.addSlide = function(t, e) {
            var n = $(t);
            i.count += 1, i.last = i.count - 1, u && c ? void 0 !== e ? i.slides.eq(i.count - e).after(n) : i.container.prepend(n) : void 0 !== e ? i.slides.eq(e).before(n) : i.container.append(n), i.update(e, "add"), i.slides = $(i.vars.selector + ":not(.clone)", i), i.setup(), i.vars.added(i)
        }, i.removeSlide = function(t) {
            var e = isNaN(t) ? i.slides.index($(t)) : t;
            i.count -= 1, i.last = i.count - 1, isNaN(t) ? $(t, i.slides).remove() : u && c ? i.slides.eq(i.last).remove() : i.slides.eq(t).remove(), i.doMath(), i.update(e, "remove"), i.slides = $(i.vars.selector + ":not(.clone)", i), i.setup(), i.vars.removed(i)
        }, f.init()
    }, $(window).blur(function(t) {
        focused = !1
    }).focus(function(t) {
        focused = !0
    }), $.flexslider.defaults = {
        namespace: "flex-",
        selector: ".slides > li",
        animation: "fade",
        easing: "swing",
        direction: "horizontal",
        reverse: !1,
        animationLoop: !0,
        smoothHeight: !1,
        startAt: 0,
        slideshow: !0,
        slideshowSpeed: 7e3,
        animationSpeed: 600,
        initDelay: 0,
        randomize: !1,
        fadeFirstSlide: !0,
        thumbCaptions: !1,
        pauseOnAction: !0,
        pauseOnHover: !1,
        pauseInvisible: !0,
        useCSS: !0,
        touch: !0,
        video: !1,
        controlNav: !0,
        directionNav: !0,
        prevText: "Previous",
        nextText: "Next",
        keyboard: !0,
        multipleKeyboard: !1,
        mousewheel: !1,
        pausePlay: !1,
        pauseText: "Pause",
        playText: "Play",
        controlsContainer: "",
        manualControls: "",
        sync: "",
        asNavFor: "",
        itemWidth: 0,
        itemMargin: 0,
        minItems: 1,
        maxItems: 0,
        move: 0,
        allowOneSlide: !0,
        start: function() {},
        before: function() {},
        after: function() {},
        end: function() {},
        added: function() {},
        removed: function() {},
        init: function() {}
    }, $.fn.flexslider = function(t) {
        if (void 0 === t && (t = {}), "object" == typeof t) return this.each(function() {
            var e = $(this),
                i = t.selector ? t.selector : ".slides > li",
                n = e.find(i);
            1 === n.length && t.allowOneSlide === !0 || 0 === n.length ? (n.fadeIn(400), t.start && t.start(e)) : void 0 === e.data("flexslider") && new $.flexslider(this, t)
        });
        var e = $(this).data("flexslider");
        switch (t) {
            case "play":
                e.play();
                break;
            case "pause":
                e.pause();
                break;
            case "stop":
                e.stop();
                break;
            case "next":
                e.flexAnimate(e.getTarget("next"), !0);
                break;
            case "prev":
            case "previous":
                e.flexAnimate(e.getTarget("prev"), !0);
                break;
            default:
                "number" == typeof t && e.flexAnimate(t, !0)
        }
    }
}(jQuery),
function($, t, e, i) {
    "use strict";

    function n(t, e) {
        this.element = t, this.$el = $(t), this.options = $.extend({}, s, e), this._defaults = s, this._name = o, this.moveInterval, this.state = 0, this.paused = 0, this.moving = 0, this.$el.is("ul, ol") && this.init()
    }
    var o = "newsTicker",
        s = {
            row_height: 20,
            max_rows: 3,
            speed: 400,
            duration: 2500,
            direction: "up",
            autostart: 1,
            pauseOnHover: 1,
            nextButton: null,
            prevButton: null,
            startButton: null,
            stopButton: null,
            hasMoved: function() {},
            movingUp: function() {},
            movingDown: function() {},
            start: function() {},
            stop: function() {},
            pause: function() {},
            unpause: function() {}
        };
    n.prototype = {
        init: function() {
            this.$el.height(this.options.row_height * this.options.max_rows).css({
                overflow: "hidden"
            }), this.checkSpeed(), this.options.nextButton && "undefined" != typeof this.options.nextButton[0] && this.options.nextButton.click(function(t) {
                this.moveNext(), this.resetInterval()
            }.bind(this)), this.options.prevButton && "undefined" != typeof this.options.prevButton[0] && this.options.prevButton.click(function(t) {
                this.movePrev(), this.resetInterval()
            }.bind(this)), this.options.stopButton && "undefined" != typeof this.options.stopButton[0] && this.options.stopButton.click(function(t) {
                this.stop()
            }.bind(this)), this.options.startButton && "undefined" != typeof this.options.startButton[0] && this.options.startButton.click(function(t) {
                this.start()
            }.bind(this)), this.options.pauseOnHover && this.$el.hover(function() {
                this.state && this.pause()
            }.bind(this), function() {
                this.state && this.unpause()
            }.bind(this)), this.options.autostart && this.start()
        },
        start: function() {
            this.state || (this.state = 1, this.resetInterval(), this.options.start())
        },
        stop: function() {
            this.state && (clearInterval(this.moveInterval), this.state = 0, this.options.stop())
        },
        resetInterval: function() {
            this.state && (clearInterval(this.moveInterval), this.moveInterval = setInterval(function() {
                this.move()
            }.bind(this), this.options.duration))
        },
        move: function() {
            this.paused || this.moveNext()
        },
        moveNext: function() {
            "down" === this.options.direction ? this.moveDown() : "up" === this.options.direction && this.moveUp()
        },
        movePrev: function() {
            "down" === this.options.direction ? this.moveUp() : "up" === this.options.direction && this.moveDown()
        },
        pause: function() {
            this.paused || (this.paused = 1), this.options.pause()
        },
        unpause: function() {
            this.paused && (this.paused = 0), this.options.unpause()
        },
        moveDown: function() {
            this.moving || (this.moving = 1, this.options.movingDown(), this.$el.children("li:last").detach().prependTo(this.$el).css("marginTop", "-" + this.options.row_height + "px").animate({
                marginTop: "0px"
            }, this.options.speed, function() {
                this.moving = 0, this.options.hasMoved()
            }.bind(this)))
        },
        moveUp: function() {
            if (!this.moving) {
                this.moving = 1, this.options.movingUp();
                var t = this.$el.children("li:first");
                t.animate({
                    marginTop: "-" + this.options.row_height + "px"
                }, this.options.speed, function() {
                    t.detach().css("marginTop", "0").appendTo(this.$el), this.moving = 0, this.options.hasMoved()
                }.bind(this))
            }
        },
        updateOption: function(t, e) {
            "undefined" != typeof this.options[t] && (this.options[t] = e, ("duration" == t || "speed" == t) && (this.checkSpeed(), this.resetInterval()))
        },
        add: function(t) {
            this.$el.append($("<li>").html(t))
        },
        getState: function() {
            return paused ? 2 : this.state
        },
        checkSpeed: function() {
            this.options.duration < this.options.speed + 25 && (this.options.speed = this.options.duration - 25)
        },
        destroy: function() {
            this._destroy()
        }
    }, $.fn[o] = function(t) {
        var e = arguments;
        return this.each(function() {
            var i = $(this),
                s = $.data(this, "plugin_" + o),
                r = "object" == typeof t && t;
            s || i.data("plugin_" + o, s = new n(this, r)), "string" == typeof t && s[t].apply(s, Array.prototype.slice.call(e, 1))
        })
    }
}(jQuery, window, document),
function(t) {
    "function" == typeof define && define.amd ? define(["jquery"], t) : "object" == typeof exports ? module.exports = t : t(jQuery)
}(function($) {
    function t(t) {
        var n = t || window.event,
            o = s.call(arguments, 1),
            l = 0,
            u = 0,
            c = 0,
            h = 0;
        if (t = $.event.fix(n), t.type = "mousewheel", "detail" in n && (c = -1 * n.detail), "wheelDelta" in n && (c = n.wheelDelta), "wheelDeltaY" in n && (c = n.wheelDeltaY), "wheelDeltaX" in n && (u = -1 * n.wheelDeltaX), "axis" in n && n.axis === n.HORIZONTAL_AXIS && (u = -1 * c, c = 0), l = 0 === c ? u : c, "deltaY" in n && (c = -1 * n.deltaY, l = c), "deltaX" in n && (u = n.deltaX, 0 === c && (l = -1 * u)), 0 !== c || 0 !== u) {
            if (1 === n.deltaMode) {
                var d = $.data(this, "mousewheel-line-height");
                l *= d, c *= d, u *= d
            } else if (2 === n.deltaMode) {
                var p = $.data(this, "mousewheel-page-height");
                l *= p, c *= p, u *= p
            }
            return h = Math.max(Math.abs(c), Math.abs(u)), (!a || a > h) && (a = h, i(n, h) && (a /= 40)), i(n, h) && (l /= 40, u /= 40, c /= 40), l = Math[l >= 1 ? "floor" : "ceil"](l / a), u = Math[u >= 1 ? "floor" : "ceil"](u / a), c = Math[c >= 1 ? "floor" : "ceil"](c / a), t.deltaX = u, t.deltaY = c, t.deltaFactor = a, t.deltaMode = 0, o.unshift(t, l, u, c), r && clearTimeout(r), r = setTimeout(e, 200), ($.event.dispatch || $.event.handle).apply(this, o)
        }
    }

    function e() {
        a = null
    }

    function i(t, e) {
        return u.settings.adjustOldDeltas && "mousewheel" === t.type && e % 120 === 0
    }
    var n = ["wheel", "mousewheel", "DOMMouseScroll", "MozMousePixelScroll"],
        o = "onwheel" in document || document.documentMode >= 9 ? ["wheel"] : ["mousewheel", "DomMouseScroll", "MozMousePixelScroll"],
        s = Array.prototype.slice,
        r, a;
    if ($.event.fixHooks)
        for (var l = n.length; l;) $.event.fixHooks[n[--l]] = $.event.mouseHooks;
    var u = $.event.special.mousewheel = {
        version: "3.1.9",
        setup: function() {
            if (this.addEventListener)
                for (var e = o.length; e;) this.addEventListener(o[--e], t, !1);
            else this.onmousewheel = t;
            $.data(this, "mousewheel-line-height", u.getLineHeight(this)), $.data(this, "mousewheel-page-height", u.getPageHeight(this))
        },
        teardown: function() {
            if (this.removeEventListener)
                for (var e = o.length; e;) this.removeEventListener(o[--e], t, !1);
            else this.onmousewheel = null
        },
        getLineHeight: function(t) {
            return parseInt($(t)["offsetParent" in $.fn ? "offsetParent" : "parent"]().css("fontSize"), 10)
        },
        getPageHeight: function(t) {
            return $(t).height()
        },
        settings: {
            adjustOldDeltas: !0
        }
    };
    $.fn.extend({
        mousewheel: function(t) {
            return t ? this.bind("mousewheel", t) : this.trigger("mousewheel")
        },
        unmousewheel: function(t) {
            return this.unbind("mousewheel", t)
        }
    })
}), ! function(t, e, i, n) {
    function o(e, i) {
        this.element = e, this.options = t.extend({}, r, i), this._defaults = r, this._name = s, this.init()
    }
    var s = "stellar",
        r = {
            scrollProperty: "scroll",
            positionProperty: "position",
            horizontalScrolling: !0,
            verticalScrolling: !0,
            horizontalOffset: 0,
            verticalOffset: 0,
            responsive: !1,
            parallaxBackgrounds: !0,
            parallaxElements: !0,
            hideDistantElements: !0,
            hideElement: function(t) {
                t.hide()
            },
            showElement: function(t) {
                t.show()
            }
        },
        a = {
            scroll: {
                getLeft: function(t) {
                    return t.scrollLeft()
                },
                setLeft: function(t, e) {
                    t.scrollLeft(e)
                },
                getTop: function(t) {
                    return t.scrollTop()
                },
                setTop: function(t, e) {
                    t.scrollTop(e)
                }
            },
            position: {
                getLeft: function(t) {
                    return -1 * parseInt(t.css("left"), 10)
                },
                getTop: function(t) {
                    return -1 * parseInt(t.css("top"), 10)
                }
            },
            margin: {
                getLeft: function(t) {
                    return -1 * parseInt(t.css("margin-left"), 10)
                },
                getTop: function(t) {
                    return -1 * parseInt(t.css("margin-top"), 10)
                }
            },
            transform: {
                getLeft: function(t) {
                    var e = getComputedStyle(t[0])[c];
                    return "none" !== e ? -1 * parseInt(e.match(/(-?[0-9]+)/g)[4], 10) : 0
                },
                getTop: function(t) {
                    var e = getComputedStyle(t[0])[c];
                    return "none" !== e ? -1 * parseInt(e.match(/(-?[0-9]+)/g)[5], 10) : 0
                }
            }
        },
        l = {
            position: {
                setLeft: function(t, e) {
                    t.css("left", e)
                },
                setTop: function(t, e) {
                    t.css("top", e)
                }
            },
            transform: {
                setPosition: function(t, e, i, n, o) {
                    t[0].style[c] = "translate3d(" + (e - i) + "px, " + (n - o) + "px, 0)"
                }
            }
        },
        u = function() {
            var e, i = /^(Moz|Webkit|Khtml|O|ms|Icab)(?=[A-Z])/,
                n = t("script")[0].style,
                o = "";
            for (e in n)
                if (i.test(e)) {
                    o = e.match(i)[0];
                    break
                }
            return "WebkitOpacity" in n && (o = "Webkit"), "KhtmlOpacity" in n && (o = "Khtml"),
                function(t) {
                    return o + (o.length > 0 ? t.charAt(0).toUpperCase() + t.slice(1) : t)
                }
        }(),
        c = u("transform"),
        h = t("<div />", {
            style: "background:#fff"
        }).css("background-position-x") !== n,
        d = h ? function(t, e, i) {
            t.css({
                "background-position-x": e,
                "background-position-y": i
            })
        } : function(t, e, i) {
            t.css("background-position", e + " " + i)
        },
        p = h ? function(t) {
            return [t.css("background-position-x"), t.css("background-position-y")]
        } : function(t) {
            return t.css("background-position").split(" ")
        },
        f = e.requestAnimationFrame || e.webkitRequestAnimationFrame || e.mozRequestAnimationFrame || e.oRequestAnimationFrame || e.msRequestAnimationFrame || function(t) {
            setTimeout(t, 1e3 / 60)
        };
    o.prototype = {
        init: function() {
            this.options.name = s + "_" + Math.floor(1e9 * Math.random()), this._defineElements(), this._defineGetters(), this._defineSetters(), this._handleWindowLoadAndResize(), this._detectViewport(), this.refresh({
                firstLoad: !0
            }), "scroll" === this.options.scrollProperty ? this._handleScrollEvent() : this._startAnimationLoop()
        },
        _defineElements: function() {
            this.element === i.body && (this.element = e), this.$scrollElement = t(this.element), this.$element = this.element === e ? t("body") : this.$scrollElement, this.$viewportElement = this.options.viewportElement !== n ? t(this.options.viewportElement) : this.$scrollElement[0] === e || "scroll" === this.options.scrollProperty ? this.$scrollElement : this.$scrollElement.parent()
        },
        _defineGetters: function() {
            var t = this,
                e = a[t.options.scrollProperty];
            this._getScrollLeft = function() {
                return e.getLeft(t.$scrollElement)
            }, this._getScrollTop = function() {
                return e.getTop(t.$scrollElement)
            }
        },
        _defineSetters: function() {
            var e = this,
                i = a[e.options.scrollProperty],
                n = l[e.options.positionProperty],
                o = i.setLeft,
                s = i.setTop;
            this._setScrollLeft = "function" == typeof o ? function(t) {
                o(e.$scrollElement, t)
            } : t.noop, this._setScrollTop = "function" == typeof s ? function(t) {
                s(e.$scrollElement, t)
            } : t.noop, this._setPosition = n.setPosition || function(t, i, o, s, r) {
                e.options.horizontalScrolling && n.setLeft(t, i, o), e.options.verticalScrolling && n.setTop(t, s, r)
            }
        },
        _handleWindowLoadAndResize: function() {
            var i = this,
                n = t(e);
            i.options.responsive && n.bind("load." + this.name, function() {
                i.refresh()
            }), n.bind("resize." + this.name, function() {
                i._detectViewport(), i.options.responsive && i.refresh()
            })
        },
        refresh: function(i) {
            var n = this,
                o = n._getScrollLeft(),
                s = n._getScrollTop();
            i && i.firstLoad || this._reset(), this._setScrollLeft(0), this._setScrollTop(0), this._setOffsets(), this._findParticles(), this._findBackgrounds(), i && i.firstLoad && /WebKit/.test(navigator.userAgent) && t(e).load(function() {
                var t = n._getScrollLeft(),
                    e = n._getScrollTop();
                n._setScrollLeft(t + 1), n._setScrollTop(e + 1), n._setScrollLeft(t), n._setScrollTop(e)
            }), this._setScrollLeft(o), this._setScrollTop(s)
        },
        _detectViewport: function() {
            var t = this.$viewportElement.offset(),
                e = null !== t && t !== n;
            this.viewportWidth = this.$viewportElement.width(), this.viewportHeight = this.$viewportElement.height(), this.viewportOffsetTop = e ? t.top : 0, this.viewportOffsetLeft = e ? t.left : 0
        },
        _findParticles: function() {
            var e = this;
            if (this._getScrollLeft(), this._getScrollTop(), this.particles !== n)
                for (var i = this.particles.length - 1; i >= 0; i--) this.particles[i].$element.data("stellar-elementIsActive", n);
            this.particles = [], this.options.parallaxElements && this.$element.find("[data-stellar-ratio]").each(function() {
                var i, o, s, r, a, l, u, c, h, d = t(this),
                    p = 0,
                    f = 0,
                    m = 0,
                    v = 0;
                if (d.data("stellar-elementIsActive")) {
                    if (d.data("stellar-elementIsActive") !== this) return
                } else d.data("stellar-elementIsActive", this);
                e.options.showElement(d), d.data("stellar-startingLeft") ? (d.css("left", d.data("stellar-startingLeft")), d.css("top", d.data("stellar-startingTop"))) : (d.data("stellar-startingLeft", d.css("left")), d.data("stellar-startingTop", d.css("top"))), s = d.position().left, r = d.position().top, a = "auto" === d.css("margin-left") ? 0 : parseInt(d.css("margin-left"), 10), l = "auto" === d.css("margin-top") ? 0 : parseInt(d.css("margin-top"), 10), c = d.offset().left - a, h = d.offset().top - l, d.parents().each(function() {
                        var e = t(this);
                        return e.data("stellar-offset-parent") === !0 ? (p = m, f = v, u = e, !1) : (m += e.position().left, void(v += e.position().top))
                    }), i = d.data("stellar-horizontal-offset") !== n ? d.data("stellar-horizontal-offset") : u !== n && u.data("stellar-horizontal-offset") !== n ? u.data("stellar-horizontal-offset") : e.horizontalOffset,
                    o = d.data("stellar-vertical-offset") !== n ? d.data("stellar-vertical-offset") : u !== n && u.data("stellar-vertical-offset") !== n ? u.data("stellar-vertical-offset") : e.verticalOffset, e.particles.push({
                        $element: d,
                        $offsetParent: u,
                        isFixed: "fixed" === d.css("position"),
                        horizontalOffset: i,
                        verticalOffset: o,
                        startingPositionLeft: s,
                        startingPositionTop: r,
                        startingOffsetLeft: c,
                        startingOffsetTop: h,
                        parentOffsetLeft: p,
                        parentOffsetTop: f,
                        stellarRatio: d.data("stellar-ratio") !== n ? d.data("stellar-ratio") : 1,
                        width: d.outerWidth(!0),
                        height: d.outerHeight(!0),
                        isHidden: !1
                    })
            })
        },
        _findBackgrounds: function() {
            var e, i = this,
                o = this._getScrollLeft(),
                s = this._getScrollTop();
            this.backgrounds = [], this.options.parallaxBackgrounds && (e = this.$element.find("[data-stellar-background-ratio]"), this.$element.data("stellar-background-ratio") && (e = e.add(this.$element)), e.each(function() {
                var e, r, a, l, u, c, h, f = t(this),
                    m = p(f),
                    v = 0,
                    g = 0,
                    y = 0,
                    b = 0;
                if (f.data("stellar-backgroundIsActive")) {
                    if (f.data("stellar-backgroundIsActive") !== this) return
                } else f.data("stellar-backgroundIsActive", this);
                f.data("stellar-backgroundStartingLeft") ? d(f, f.data("stellar-backgroundStartingLeft"), f.data("stellar-backgroundStartingTop")) : (f.data("stellar-backgroundStartingLeft", m[0]), f.data("stellar-backgroundStartingTop", m[1])), a = "auto" === f.css("margin-left") ? 0 : parseInt(f.css("margin-left"), 10), l = "auto" === f.css("margin-top") ? 0 : parseInt(f.css("margin-top"), 10), u = f.offset().left - a - o, c = f.offset().top - l - s, f.parents().each(function() {
                    var e = t(this);
                    return e.data("stellar-offset-parent") === !0 ? (v = y, g = b, h = e, !1) : (y += e.position().left, void(b += e.position().top))
                }), e = f.data("stellar-horizontal-offset") !== n ? f.data("stellar-horizontal-offset") : h !== n && h.data("stellar-horizontal-offset") !== n ? h.data("stellar-horizontal-offset") : i.horizontalOffset, r = f.data("stellar-vertical-offset") !== n ? f.data("stellar-vertical-offset") : h !== n && h.data("stellar-vertical-offset") !== n ? h.data("stellar-vertical-offset") : i.verticalOffset, i.backgrounds.push({
                    $element: f,
                    $offsetParent: h,
                    isFixed: "fixed" === f.css("background-attachment"),
                    horizontalOffset: e,
                    verticalOffset: r,
                    startingValueLeft: m[0],
                    startingValueTop: m[1],
                    startingBackgroundPositionLeft: isNaN(parseInt(m[0], 10)) ? 0 : parseInt(m[0], 10),
                    startingBackgroundPositionTop: isNaN(parseInt(m[1], 10)) ? 0 : parseInt(m[1], 10),
                    startingPositionLeft: f.position().left,
                    startingPositionTop: f.position().top,
                    startingOffsetLeft: u,
                    startingOffsetTop: c,
                    parentOffsetLeft: v,
                    parentOffsetTop: g,
                    stellarRatio: f.data("stellar-background-ratio") === n ? 1 : f.data("stellar-background-ratio")
                })
            }))
        },
        _reset: function() {
            var t, e, i, n, o;
            for (o = this.particles.length - 1; o >= 0; o--) t = this.particles[o], e = t.$element.data("stellar-startingLeft"), i = t.$element.data("stellar-startingTop"), this._setPosition(t.$element, e, e, i, i), this.options.showElement(t.$element), t.$element.data("stellar-startingLeft", null).data("stellar-elementIsActive", null).data("stellar-backgroundIsActive", null);
            for (o = this.backgrounds.length - 1; o >= 0; o--) n = this.backgrounds[o], n.$element.data("stellar-backgroundStartingLeft", null).data("stellar-backgroundStartingTop", null), d(n.$element, n.startingValueLeft, n.startingValueTop)
        },
        destroy: function() {
            this._reset(), this.$scrollElement.unbind("resize." + this.name).unbind("scroll." + this.name), this._animationLoop = t.noop, t(e).unbind("load." + this.name).unbind("resize." + this.name)
        },
        _setOffsets: function() {
            var i = this,
                n = t(e);
            n.unbind("resize.horizontal-" + this.name).unbind("resize.vertical-" + this.name), "function" == typeof this.options.horizontalOffset ? (this.horizontalOffset = this.options.horizontalOffset(), n.bind("resize.horizontal-" + this.name, function() {
                i.horizontalOffset = i.options.horizontalOffset()
            })) : this.horizontalOffset = this.options.horizontalOffset, "function" == typeof this.options.verticalOffset ? (this.verticalOffset = this.options.verticalOffset(), n.bind("resize.vertical-" + this.name, function() {
                i.verticalOffset = i.options.verticalOffset()
            })) : this.verticalOffset = this.options.verticalOffset
        },
        _repositionElements: function() {
            var t, e, i, n, o, s, r, a, l, u, c = this._getScrollLeft(),
                h = this._getScrollTop(),
                p = !0,
                f = !0;
            if (this.currentScrollLeft !== c || this.currentScrollTop !== h || this.currentWidth !== this.viewportWidth || this.currentHeight !== this.viewportHeight) {
                for (this.currentScrollLeft = c, this.currentScrollTop = h, this.currentWidth = this.viewportWidth, this.currentHeight = this.viewportHeight, u = this.particles.length - 1; u >= 0; u--) t = this.particles[u], e = t.isFixed ? 1 : 0, this.options.horizontalScrolling ? (s = (c + t.horizontalOffset + this.viewportOffsetLeft + t.startingPositionLeft - t.startingOffsetLeft + t.parentOffsetLeft) * -(t.stellarRatio + e - 1) + t.startingPositionLeft, a = s - t.startingPositionLeft + t.startingOffsetLeft) : (s = t.startingPositionLeft, a = t.startingOffsetLeft), this.options.verticalScrolling ? (r = (h + t.verticalOffset + this.viewportOffsetTop + t.startingPositionTop - t.startingOffsetTop + t.parentOffsetTop) * -(t.stellarRatio + e - 1) + t.startingPositionTop, l = r - t.startingPositionTop + t.startingOffsetTop) : (r = t.startingPositionTop, l = t.startingOffsetTop), this.options.hideDistantElements && (f = !this.options.horizontalScrolling || a + t.width > (t.isFixed ? 0 : c) && a < (t.isFixed ? 0 : c) + this.viewportWidth + this.viewportOffsetLeft, p = !this.options.verticalScrolling || l + t.height > (t.isFixed ? 0 : h) && l < (t.isFixed ? 0 : h) + this.viewportHeight + this.viewportOffsetTop), f && p ? (t.isHidden && (this.options.showElement(t.$element), t.isHidden = !1), this._setPosition(t.$element, s, t.startingPositionLeft, r, t.startingPositionTop)) : t.isHidden || (this.options.hideElement(t.$element), t.isHidden = !0);
                for (u = this.backgrounds.length - 1; u >= 0; u--) i = this.backgrounds[u], e = i.isFixed ? 0 : 1, n = this.options.horizontalScrolling ? (c + i.horizontalOffset - this.viewportOffsetLeft - i.startingOffsetLeft + i.parentOffsetLeft - i.startingBackgroundPositionLeft) * (e - i.stellarRatio) + "px" : i.startingValueLeft, o = this.options.verticalScrolling ? (h + i.verticalOffset - this.viewportOffsetTop - i.startingOffsetTop + i.parentOffsetTop - i.startingBackgroundPositionTop) * (e - i.stellarRatio) + "px" : i.startingValueTop, d(i.$element, n, o)
            }
        },
        _handleScrollEvent: function() {
            var t = this,
                e = !1,
                i = function() {
                    t._repositionElements(), e = !1
                },
                n = function() {
                    e || (f(i), e = !0)
                };
            this.$scrollElement.bind("scroll." + this.name, n), n()
        },
        _startAnimationLoop: function() {
            var t = this;
            this._animationLoop = function() {
                f(t._animationLoop), t._repositionElements()
            }, this._animationLoop()
        }
    }, t.fn[s] = function(e) {
        var i = arguments;
        return e === n || "object" == typeof e ? this.each(function() {
            t.data(this, "plugin_" + s) || t.data(this, "plugin_" + s, new o(this, e))
        }) : "string" == typeof e && "_" !== e[0] && "init" !== e ? this.each(function() {
            var n = t.data(this, "plugin_" + s);
            n instanceof o && "function" == typeof n[e] && n[e].apply(n, Array.prototype.slice.call(i, 1)), "destroy" === e && t.data(this, "plugin_" + s, null)
        }) : void 0
    }, t[s] = function() {
        var i = t(e);
        return i.stellar.apply(i, Array.prototype.slice.call(arguments, 0))
    }, t[s].scrollProperty = a, t[s].positionProperty = l, e.Stellar = o
}(jQuery, this, document), ! function(t) {
    var e = function() {
            "use strict";
            return {
                isMsie: function() {
                    return /(msie|trident)/i.test(navigator.userAgent) ? navigator.userAgent.match(/(msie |rv:)(\d+(.\d+)?)/i)[2] : !1
                },
                isBlankString: function(t) {
                    return !t || /^\s*$/.test(t)
                },
                escapeRegExChars: function(t) {
                    return t.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&")
                },
                isString: function(t) {
                    return "string" == typeof t
                },
                isNumber: function(t) {
                    return "number" == typeof t
                },
                isArray: t.isArray,
                isFunction: t.isFunction,
                isObject: t.isPlainObject,
                isUndefined: function(t) {
                    return "undefined" == typeof t
                },
                toStr: function(t) {
                    return e.isUndefined(t) || null === t ? "" : t + ""
                },
                bind: t.proxy,
                each: function(e, i) {
                    function n(t, e) {
                        return i(e, t)
                    }
                    t.each(e, n)
                },
                map: t.map,
                filter: t.grep,
                every: function(e, i) {
                    var n = !0;
                    return e ? (t.each(e, function(t, o) {
                        return (n = i.call(null, o, t, e)) ? void 0 : !1
                    }), !!n) : n
                },
                some: function(e, i) {
                    var n = !1;
                    return e ? (t.each(e, function(t, o) {
                        return (n = i.call(null, o, t, e)) ? !1 : void 0
                    }), !!n) : n
                },
                mixin: t.extend,
                getUniqueId: function() {
                    var t = 0;
                    return function() {
                        return t++
                    }
                }(),
                templatify: function(e) {
                    function i() {
                        return String(e)
                    }
                    return t.isFunction(e) ? e : i
                },
                defer: function(t) {
                    setTimeout(t, 0)
                },
                debounce: function(t, e, i) {
                    var n, o;
                    return function() {
                        var s, r, a = this,
                            l = arguments;
                        return s = function() {
                            n = null, i || (o = t.apply(a, l))
                        }, r = i && !n, clearTimeout(n), n = setTimeout(s, e), r && (o = t.apply(a, l)), o
                    }
                },
                throttle: function(t, e) {
                    var i, n, o, s, r, a;
                    return r = 0, a = function() {
                            r = new Date, o = null, s = t.apply(i, n)
                        },
                        function() {
                            var l = new Date,
                                u = e - (l - r);
                            return i = this, n = arguments, 0 >= u ? (clearTimeout(o), o = null, r = l, s = t.apply(i, n)) : o || (o = setTimeout(a, u)), s
                        }
                },
                noop: function() {}
            }
        }(),
        i = "0.10.5",
        n = function() {
            "use strict";

            function t(t) {
                return t = e.toStr(t), t ? t.split(/\s+/) : []
            }

            function i(t) {
                return t = e.toStr(t), t ? t.split(/\W+/) : []
            }

            function n(t) {
                return function() {
                    var i = [].slice.call(arguments, 0);
                    return function(n) {
                        var o = [];
                        return e.each(i, function(i) {
                            o = o.concat(t(e.toStr(n[i])))
                        }), o
                    }
                }
            }
            return {
                nonword: i,
                whitespace: t,
                obj: {
                    nonword: n(i),
                    whitespace: n(t)
                }
            }
        }(),
        o = function() {
            "use strict";

            function i(i) {
                this.maxSize = e.isNumber(i) ? i : 100, this.reset(), this.maxSize <= 0 && (this.set = this.get = t.noop)
            }

            function n() {
                this.head = this.tail = null
            }

            function o(t, e) {
                this.key = t, this.val = e, this.prev = this.next = null
            }
            return e.mixin(i.prototype, {
                set: function(t, e) {
                    var i, n = this.list.tail;
                    this.size >= this.maxSize && (this.list.remove(n), delete this.hash[n.key]), (i = this.hash[t]) ? (i.val = e, this.list.moveToFront(i)) : (i = new o(t, e), this.list.add(i), this.hash[t] = i, this.size++)
                },
                get: function(t) {
                    var e = this.hash[t];
                    return e ? (this.list.moveToFront(e), e.val) : void 0
                },
                reset: function() {
                    this.size = 0, this.hash = {}, this.list = new n
                }
            }), e.mixin(n.prototype, {
                add: function(t) {
                    this.head && (t.next = this.head, this.head.prev = t), this.head = t, this.tail = this.tail || t
                },
                remove: function(t) {
                    t.prev ? t.prev.next = t.next : this.head = t.next, t.next ? t.next.prev = t.prev : this.tail = t.prev
                },
                moveToFront: function(t) {
                    this.remove(t), this.add(t)
                }
            }), i
        }(),
        s = function() {
            "use strict";

            function t(t) {
                this.prefix = ["__", t, "__"].join(""), this.ttlKey = "__ttl__", this.keyMatcher = new RegExp("^" + e.escapeRegExChars(this.prefix))
            }

            function i() {
                return (new Date).getTime()
            }

            function n(t) {
                return JSON.stringify(e.isUndefined(t) ? null : t)
            }

            function o(t) {
                return JSON.parse(t)
            }
            var s, r;
            try {
                s = window.localStorage, s.setItem("~~~", "!"), s.removeItem("~~~")
            } catch (a) {
                s = null
            }
            return r = s && window.JSON ? {
                _prefix: function(t) {
                    return this.prefix + t
                },
                _ttlKey: function(t) {
                    return this._prefix(t) + this.ttlKey
                },
                get: function(t) {
                    return this.isExpired(t) && this.remove(t), o(s.getItem(this._prefix(t)))
                },
                set: function(t, o, r) {
                    return e.isNumber(r) ? s.setItem(this._ttlKey(t), n(i() + r)) : s.removeItem(this._ttlKey(t)), s.setItem(this._prefix(t), n(o))
                },
                remove: function(t) {
                    return s.removeItem(this._ttlKey(t)), s.removeItem(this._prefix(t)), this
                },
                clear: function() {
                    var t, e, i = [],
                        n = s.length;
                    for (t = 0; n > t; t++)(e = s.key(t)).match(this.keyMatcher) && i.push(e.replace(this.keyMatcher, ""));
                    for (t = i.length; t--;) this.remove(i[t]);
                    return this
                },
                isExpired: function(t) {
                    var n = o(s.getItem(this._ttlKey(t)));
                    return e.isNumber(n) && i() > n ? !0 : !1
                }
            } : {
                get: e.noop,
                set: e.noop,
                remove: e.noop,
                clear: e.noop,
                isExpired: e.noop
            }, e.mixin(t.prototype, r), t
        }(),
        r = function() {
            "use strict";

            function i(e) {
                e = e || {}, this.cancelled = !1, this.lastUrl = null, this._send = e.transport ? n(e.transport) : t.ajax, this._get = e.rateLimiter ? e.rateLimiter(this._get) : this._get, this._cache = e.cache === !1 ? new o(0) : l
            }

            function n(i) {
                return function(n, o) {
                    function s(t) {
                        e.defer(function() {
                            a.resolve(t)
                        })
                    }

                    function r(t) {
                        e.defer(function() {
                            a.reject(t)
                        })
                    }
                    var a = t.Deferred();
                    return i(n, o, s, r), a
                }
            }
            var s = 0,
                r = {},
                a = 6,
                l = new o(10);
            return i.setMaxPendingRequests = function(t) {
                a = t
            }, i.resetCache = function() {
                l.reset()
            }, e.mixin(i.prototype, {
                _get: function(t, e, i) {
                    function n(e) {
                        i && i(null, e), c._cache.set(t, e)
                    }

                    function o() {
                        i && i(!0)
                    }

                    function l() {
                        s--, delete r[t], c.onDeckRequestArgs && (c._get.apply(c, c.onDeckRequestArgs), c.onDeckRequestArgs = null)
                    }
                    var u, c = this;
                    this.cancelled || t !== this.lastUrl || ((u = r[t]) ? u.done(n).fail(o) : a > s ? (s++, r[t] = this._send(t, e).done(n).fail(o).always(l)) : this.onDeckRequestArgs = [].slice.call(arguments, 0))
                },
                get: function(t, i, n) {
                    var o;
                    return e.isFunction(i) && (n = i, i = {}), this.cancelled = !1, this.lastUrl = t, (o = this._cache.get(t)) ? e.defer(function() {
                        n && n(null, o)
                    }) : this._get(t, i, n), !!o
                },
                cancel: function() {
                    this.cancelled = !0
                }
            }), i
        }(),
        a = function() {
            "use strict";

            function i(e) {
                e = e || {}, e.datumTokenizer && e.queryTokenizer || t.error("datumTokenizer and queryTokenizer are both required"), this.datumTokenizer = e.datumTokenizer, this.queryTokenizer = e.queryTokenizer, this.reset()
            }

            function n(t) {
                return t = e.filter(t, function(t) {
                    return !!t
                }), t = e.map(t, function(t) {
                    return t.toLowerCase()
                })
            }

            function o() {
                return {
                    ids: [],
                    children: {}
                }
            }

            function s(t) {
                for (var e = {}, i = [], n = 0, o = t.length; o > n; n++) e[t[n]] || (e[t[n]] = !0, i.push(t[n]));
                return i
            }

            function r(t, e) {
                function i(t, e) {
                    return t - e
                }
                var n = 0,
                    o = 0,
                    s = [];
                t = t.sort(i), e = e.sort(i);
                for (var r = t.length, a = e.length; r > n && a > o;) t[n] < e[o] ? n++ : t[n] > e[o] ? o++ : (s.push(t[n]), n++, o++);
                return s
            }
            return e.mixin(i.prototype, {
                bootstrap: function(t) {
                    this.datums = t.datums, this.trie = t.trie
                },
                add: function(t) {
                    var i = this;
                    t = e.isArray(t) ? t : [t], e.each(t, function(t) {
                        var s, r;
                        s = i.datums.push(t) - 1, r = n(i.datumTokenizer(t)), e.each(r, function(t) {
                            var e, n, r;
                            for (e = i.trie, n = t.split(""); r = n.shift();) e = e.children[r] || (e.children[r] = o()), e.ids.push(s)
                        })
                    })
                },
                get: function(t) {
                    var i, o, a = this;
                    return i = n(this.queryTokenizer(t)), e.each(i, function(t) {
                        var e, i, n, s;
                        if (o && 0 === o.length) return !1;
                        for (e = a.trie, i = t.split(""); e && (n = i.shift());) e = e.children[n];
                        return e && 0 === i.length ? (s = e.ids.slice(0), void(o = o ? r(o, s) : s)) : (o = [], !1)
                    }), o ? e.map(s(o), function(t) {
                        return a.datums[t]
                    }) : []
                },
                reset: function() {
                    this.datums = [], this.trie = o()
                },
                serialize: function() {
                    return {
                        datums: this.datums,
                        trie: this.trie
                    }
                }
            }), i
        }(),
        l = function() {
            "use strict";

            function n(t) {
                return t.local || null
            }

            function o(n) {
                var o, s;
                return s = {
                    url: null,
                    thumbprint: "",
                    ttl: 864e5,
                    filter: null,
                    ajax: {}
                }, (o = n.prefetch || null) && (o = e.isString(o) ? {
                    url: o
                } : o, o = e.mixin(s, o), o.thumbprint = i + o.thumbprint, o.ajax.type = o.ajax.type || "GET", o.ajax.dataType = o.ajax.dataType || "json", !o.url && t.error("prefetch requires url to be set")), o
            }

            function s(i) {
                function n(t) {
                    return function(i) {
                        return e.debounce(i, t)
                    }
                }

                function o(t) {
                    return function(i) {
                        return e.throttle(i, t)
                    }
                }
                var s, r;
                return r = {
                    url: null,
                    cache: !0,
                    wildcard: "%QUERY",
                    replace: null,
                    rateLimitBy: "debounce",
                    rateLimitWait: 300,
                    send: null,
                    filter: null,
                    ajax: {}
                }, (s = i.remote || null) && (s = e.isString(s) ? {
                    url: s
                } : s, s = e.mixin(r, s), s.rateLimiter = /^throttle$/i.test(s.rateLimitBy) ? o(s.rateLimitWait) : n(s.rateLimitWait), s.ajax.type = s.ajax.type || "GET", s.ajax.dataType = s.ajax.dataType || "json", delete s.rateLimitBy, delete s.rateLimitWait, !s.url && t.error("remote requires url to be set")), s
            }
            return {
                local: n,
                prefetch: o,
                remote: s
            }
        }();
    ! function(i) {
        "use strict";

        function o(e) {
            e && (e.local || e.prefetch || e.remote) || t.error("one of local, prefetch, or remote is required"), this.limit = e.limit || 5, this.sorter = u(e.sorter), this.dupDetector = e.dupDetector || c, this.local = l.local(e), this.prefetch = l.prefetch(e), this.remote = l.remote(e), this.cacheKey = this.prefetch ? this.prefetch.cacheKey || this.prefetch.url : null, this.index = new a({
                datumTokenizer: e.datumTokenizer,
                queryTokenizer: e.queryTokenizer
            }), this.storage = this.cacheKey ? new s(this.cacheKey) : null
        }

        function u(t) {
            function i(e) {
                return e.sort(t)
            }

            function n(t) {
                return t
            }
            return e.isFunction(t) ? i : n
        }

        function c() {
            return !1
        }
        var h, d;
        return h = i.Bloodhound, d = {
            data: "data",
            protocol: "protocol",
            thumbprint: "thumbprint"
        }, i.Bloodhound = o, o.noConflict = function() {
            return i.Bloodhound = h, o
        }, o.tokenizers = n, e.mixin(o.prototype, {
            _loadPrefetch: function(e) {
                function i(t) {
                    s.clear(), s.add(e.filter ? e.filter(t) : t), s._saveToStorage(s.index.serialize(), e.thumbprint, e.ttl)
                }
                var n, o, s = this;
                return (n = this._readFromStorage(e.thumbprint)) ? (this.index.bootstrap(n), o = t.Deferred().resolve()) : o = t.ajax(e.url, e.ajax).done(i), o
            },
            _getFromRemote: function(t, e) {
                function i(t, i) {
                    e(t ? [] : s.remote.filter ? s.remote.filter(i) : i)
                }
                var n, o, s = this;
                return this.transport ? (t = t || "", o = encodeURIComponent(t), n = this.remote.replace ? this.remote.replace(this.remote.url, t) : this.remote.url.replace(this.remote.wildcard, o), this.transport.get(n, this.remote.ajax, i)) : void 0
            },
            _cancelLastRemoteRequest: function() {
                this.transport && this.transport.cancel()
            },
            _saveToStorage: function(t, e, i) {
                this.storage && (this.storage.set(d.data, t, i), this.storage.set(d.protocol, location.protocol, i), this.storage.set(d.thumbprint, e, i))
            },
            _readFromStorage: function(t) {
                var e, i = {};
                return this.storage && (i.data = this.storage.get(d.data), i.protocol = this.storage.get(d.protocol), i.thumbprint = this.storage.get(d.thumbprint)), e = i.thumbprint !== t || i.protocol !== location.protocol, i.data && !e ? i.data : null
            },
            _initialize: function() {
                function i() {
                    o.add(e.isFunction(s) ? s() : s)
                }
                var n, o = this,
                    s = this.local;
                return n = this.prefetch ? this._loadPrefetch(this.prefetch) : t.Deferred().resolve(), s && n.done(i), this.transport = this.remote ? new r(this.remote) : null, this.initPromise = n.promise()
            },
            initialize: function(t) {
                return !this.initPromise || t ? this._initialize() : this.initPromise
            },
            add: function(t) {
                this.index.add(t)
            },
            get: function(t, i) {
                function n(t) {
                    var n = s.slice(0);
                    e.each(t, function(t) {
                        var i;
                        return i = e.some(n, function(e) {
                            return o.dupDetector(t, e)
                        }), !i && n.push(t), n.length < o.limit
                    }), i && i(o.sorter(n))
                }
                var o = this,
                    s = [],
                    r = !1;
                s = this.index.get(t), s = this.sorter(s).slice(0, this.limit), s.length < this.limit ? r = this._getFromRemote(t, n) : this._cancelLastRemoteRequest(), r || (s.length > 0 || !this.transport) && i && i(s)
            },
            clear: function() {
                this.index.reset()
            },
            clearPrefetchCache: function() {
                this.storage && this.storage.clear()
            },
            clearRemoteCache: function() {
                this.transport && r.resetCache()
            },
            ttAdapter: function() {
                return e.bind(this.get, this)
            }
        }), o
    }(this);
    var u = function() {
            return {
                wrapper: '<span class="twitter-typeahead"></span>',
                dropdown: '<span class="tt-dropdown-menu"></span>',
                dataset: '<div class="tt-dataset-%CLASS%"></div>',
                suggestions: '<span class="tt-suggestions"></span>',
                suggestion: '<div class="tt-suggestion"></div>'
            }
        }(),
        c = function() {
            "use strict";
            var t = {
                wrapper: {
                    position: "relative",
                    display: "inline-block"
                },
                hint: {
                    position: "absolute",
                    top: "0",
                    left: "0",
                    borderColor: "transparent",
                    boxShadow: "none",
                    opacity: "1"
                },
                input: {
                    position: "relative",
                    verticalAlign: "top",
                    backgroundColor: "transparent"
                },
                inputWithNoHint: {
                    position: "relative",
                    verticalAlign: "top"
                },
                dropdown: {
                    position: "absolute",
                    top: "100%",
                    left: "0",
                    zIndex: "100",
                    display: "none"
                },
                suggestions: {
                    display: "block"
                },
                suggestion: {
                    whiteSpace: "nowrap",
                    cursor: "pointer"
                },
                suggestionChild: {
                    whiteSpace: "normal"
                },
                ltr: {
                    left: "0",
                    right: "auto"
                },
                rtl: {
                    left: "auto",
                    right: " 0"
                }
            };
            return e.isMsie() && e.mixin(t.input, {
                backgroundImage: "url(data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)"
            }), e.isMsie() && e.isMsie() <= 7 && e.mixin(t.input, {
                marginTop: "-1px"
            }), t
        }(),
        h = function() {
            "use strict";

            function i(e) {
                e && e.el || t.error("EventBus initialized without el"), this.$el = t(e.el)
            }
            var n = "typeahead:";
            return e.mixin(i.prototype, {
                trigger: function(t) {
                    var e = [].slice.call(arguments, 1);
                    this.$el.trigger(n + t, e)
                }
            }), i
        }(),
        d = function() {
            "use strict";

            function t(t, e, i, n) {
                var o;
                if (!i) return this;
                for (e = e.split(l), i = n ? a(i, n) : i, this._callbacks = this._callbacks || {}; o = e.shift();) this._callbacks[o] = this._callbacks[o] || {
                    sync: [],
                    async: []
                }, this._callbacks[o][t].push(i);
                return this
            }

            function e(e, i, n) {
                return t.call(this, "async", e, i, n)
            }

            function i(e, i, n) {
                return t.call(this, "sync", e, i, n)
            }

            function n(t) {
                var e;
                if (!this._callbacks) return this;
                for (t = t.split(l); e = t.shift();) delete this._callbacks[e];
                return this
            }

            function o(t) {
                var e, i, n, o, r;
                if (!this._callbacks) return this;
                for (t = t.split(l), n = [].slice.call(arguments, 1);
                    (e = t.shift()) && (i = this._callbacks[e]);) o = s(i.sync, this, [e].concat(n)), r = s(i.async, this, [e].concat(n)), o() && u(r);
                return this
            }

            function s(t, e, i) {
                function n() {
                    for (var n, o = 0, s = t.length; !n && s > o; o += 1) n = t[o].apply(e, i) === !1;
                    return !n
                }
                return n
            }

            function r() {
                var t;
                return t = window.setImmediate ? function(t) {
                    setImmediate(function() {
                        t()
                    })
                } : function(t) {
                    setTimeout(function() {
                        t()
                    }, 0)
                }
            }

            function a(t, e) {
                return t.bind ? t.bind(e) : function() {
                    t.apply(e, [].slice.call(arguments, 0))
                }
            }
            var l = /\s+/,
                u = r();
            return {
                onSync: i,
                onAsync: e,
                off: n,
                trigger: o
            }
        }(),
        p = function(t) {
            "use strict";

            function i(t, i, n) {
                for (var o, s = [], r = 0, a = t.length; a > r; r++) s.push(e.escapeRegExChars(t[r]));
                return o = n ? "\\b(" + s.join("|") + ")\\b" : "(" + s.join("|") + ")", i ? new RegExp(o) : new RegExp(o, "i")
            }
            var n = {
                node: null,
                pattern: null,
                tagName: "strong",
                className: null,
                wordsOnly: !1,
                caseSensitive: !1
            };
            return function(o) {
                function s(e) {
                    var i, n, s;
                    return (i = a.exec(e.data)) && (s = t.createElement(o.tagName), o.className && (s.className = o.className), n = e.splitText(i.index), n.splitText(i[0].length), s.appendChild(n.cloneNode(!0)), e.parentNode.replaceChild(s, n)), !!i
                }

                function r(t, e) {
                    for (var i, n = 3, o = 0; o < t.childNodes.length; o++) i = t.childNodes[o], i.nodeType === n ? o += e(i) ? 1 : 0 : r(i, e)
                }
                var a;
                o = e.mixin({}, n, o), o.node && o.pattern && (o.pattern = e.isArray(o.pattern) ? o.pattern : [o.pattern], a = i(o.pattern, o.caseSensitive, o.wordsOnly), r(o.node, s))
            }
        }(window.document),
        f = function() {
            "use strict";

            function i(i) {
                var o, s, a, l, u = this;
                i = i || {}, i.input || t.error("input is missing"), o = e.bind(this._onBlur, this), s = e.bind(this._onFocus, this), a = e.bind(this._onKeydown, this), l = e.bind(this._onInput, this), this.$hint = t(i.hint), this.$input = t(i.input).on("blur.tt", o).on("focus.tt", s).on("keydown.tt", a), 0 === this.$hint.length && (this.setHint = this.getHint = this.clearHint = this.clearHintIfInvalid = e.noop), e.isMsie() ? this.$input.on("keydown.tt keypress.tt cut.tt paste.tt", function(t) {
                    r[t.which || t.keyCode] || e.defer(e.bind(u._onInput, u, t))
                }) : this.$input.on("input.tt", l), this.query = this.$input.val(), this.$overflowHelper = n(this.$input)
            }

            function n(e) {
                return t('<pre aria-hidden="true"></pre>').css({
                    position: "absolute",
                    visibility: "hidden",
                    whiteSpace: "pre",
                    fontFamily: e.css("font-family"),
                    fontSize: e.css("font-size"),
                    fontStyle: e.css("font-style"),
                    fontVariant: e.css("font-variant"),
                    fontWeight: e.css("font-weight"),
                    wordSpacing: e.css("word-spacing"),
                    letterSpacing: e.css("letter-spacing"),
                    textIndent: e.css("text-indent"),
                    textRendering: e.css("text-rendering"),
                    textTransform: e.css("text-transform")
                }).insertAfter(e)
            }

            function o(t, e) {
                return i.normalizeQuery(t) === i.normalizeQuery(e)
            }

            function s(t) {
                return t.altKey || t.ctrlKey || t.metaKey || t.shiftKey
            }
            var r;
            return r = {
                9: "tab",
                27: "esc",
                37: "left",
                39: "right",
                13: "enter",
                38: "up",
                40: "down"
            }, i.normalizeQuery = function(t) {
                return (t || "").replace(/^\s*/g, "").replace(/\s{2,}/g, " ")
            }, e.mixin(i.prototype, d, {
                _onBlur: function() {
                    this.resetInputValue(), this.trigger("blurred")
                },
                _onFocus: function() {
                    this.trigger("focused")
                },
                _onKeydown: function(t) {
                    var e = r[t.which || t.keyCode];
                    this._managePreventDefault(e, t), e && this._shouldTrigger(e, t) && this.trigger(e + "Keyed", t)
                },
                _onInput: function() {
                    this._checkInputValue()
                },
                _managePreventDefault: function(t, e) {
                    var i, n, o;
                    switch (t) {
                        case "tab":
                            n = this.getHint(), o = this.getInputValue(), i = n && n !== o && !s(e);
                            break;
                        case "up":
                        case "down":
                            i = !s(e);
                            break;
                        default:
                            i = !1
                    }
                    i && e.preventDefault()
                },
                _shouldTrigger: function(t, e) {
                    var i;
                    switch (t) {
                        case "tab":
                            i = !s(e);
                            break;
                        default:
                            i = !0
                    }
                    return i
                },
                _checkInputValue: function() {
                    var t, e, i;
                    t = this.getInputValue(), e = o(t, this.query), i = e ? this.query.length !== t.length : !1, this.query = t, e ? i && this.trigger("whitespaceChanged", this.query) : this.trigger("queryChanged", this.query)
                },
                focus: function() {
                    this.$input.focus()
                },
                blur: function() {
                    this.$input.blur()
                },
                getQuery: function() {
                    return this.query
                },
                setQuery: function(t) {
                    this.query = t
                },
                getInputValue: function() {
                    return this.$input.val()
                },
                setInputValue: function(t, e) {
                    this.$input.val(t), e ? this.clearHint() : this._checkInputValue()
                },
                resetInputValue: function() {
                    this.setInputValue(this.query, !0)
                },
                getHint: function() {
                    return this.$hint.val()
                },
                setHint: function(t) {
                    this.$hint.val(t)
                },
                clearHint: function() {
                    this.setHint("")
                },
                clearHintIfInvalid: function() {
                    var t, e, i, n;
                    t = this.getInputValue(), e = this.getHint(), i = t !== e && 0 === e.indexOf(t), n = "" !== t && i && !this.hasOverflow(), !n && this.clearHint()
                },
                getLanguageDirection: function() {
                    return (this.$input.css("direction") || "ltr").toLowerCase()
                },
                hasOverflow: function() {
                    var t = this.$input.width() - 2;
                    return this.$overflowHelper.text(this.getInputValue()), this.$overflowHelper.width() >= t
                },
                isCursorAtEnd: function() {
                    var t, i, n;
                    return t = this.$input.val().length, i = this.$input[0].selectionStart, e.isNumber(i) ? i === t : document.selection ? (n = document.selection.createRange(), n.moveStart("character", -t), t === n.text.length) : !0
                },
                destroy: function() {
                    this.$hint.off(".tt"), this.$input.off(".tt"), this.$hint = this.$input = this.$overflowHelper = null
                }
            }), i
        }(),
        m = function() {
            "use strict";

            function i(i) {
                i = i || {}, i.templates = i.templates || {}, i.source || t.error("missing source"), i.name && !s(i.name) && t.error("invalid dataset name: " + i.name), this.query = null, this.highlight = !!i.highlight, this.name = i.name || e.getUniqueId(), this.source = i.source, this.displayFn = n(i.display || i.displayKey), this.templates = o(i.templates, this.displayFn), this.$el = t(u.dataset.replace("%CLASS%", this.name))
            }

            function n(t) {
                function i(e) {
                    return e[t]
                }
                return t = t || "value", e.isFunction(t) ? t : i
            }

            function o(t, i) {
                function n(t) {
                    return "<p>" + i(t) + "</p>"
                }
                return {
                    empty: t.empty && e.templatify(t.empty),
                    header: t.header && e.templatify(t.header),
                    footer: t.footer && e.templatify(t.footer),
                    suggestion: t.suggestion || n
                }
            }

            function s(t) {
                return /^[_a-zA-Z0-9-]+$/.test(t)
            }
            var r = "ttDataset",
                a = "ttValue",
                l = "ttDatum";
            return i.extractDatasetName = function(e) {
                return t(e).data(r)
            }, i.extractValue = function(e) {
                return t(e).data(a)
            }, i.extractDatum = function(e) {
                return t(e).data(l)
            }, e.mixin(i.prototype, d, {
                _render: function(i, n) {
                    function o() {
                        return m.templates.empty({
                            query: i,
                            isEmpty: !0
                        })
                    }

                    function s() {
                        function o(e) {
                            var i;
                            return i = t(u.suggestion).append(m.templates.suggestion(e)).data(r, m.name).data(a, m.displayFn(e)).data(l, e), i.children().each(function() {
                                t(this).css(c.suggestionChild)
                            }), i
                        }
                        var s, h;
                        return s = t(u.suggestions).css(c.suggestions), h = e.map(n, o), s.append.apply(s, h), m.highlight && p({
                            className: "tt-highlight",
                            node: s[0],
                            pattern: i
                        }), s
                    }

                    function h() {
                        return m.templates.header({
                            query: i,
                            isEmpty: !f
                        })
                    }

                    function d() {
                        return m.templates.footer({
                            query: i,
                            isEmpty: !f
                        })
                    }
                    if (this.$el) {
                        var f, m = this;
                        this.$el.empty(), f = n && n.length, !f && this.templates.empty ? this.$el.html(o()).prepend(m.templates.header ? h() : null).append(m.templates.footer ? d() : null) : f && this.$el.html(s()).prepend(m.templates.header ? h() : null).append(m.templates.footer ? d() : null), this.trigger("rendered")
                    }
                },
                getRoot: function() {
                    return this.$el
                },
                update: function(t) {
                    function e(e) {
                        i.canceled || t !== i.query || i._render(t, e)
                    }
                    var i = this;
                    this.query = t, this.canceled = !1, this.source(t, e)
                },
                cancel: function() {
                    this.canceled = !0
                },
                clear: function() {
                    this.cancel(), this.$el.empty(), this.trigger("rendered")
                },
                isEmpty: function() {
                    return this.$el.is(":empty")
                },
                destroy: function() {
                    this.$el = null
                }
            }), i
        }(),
        v = function() {
            "use strict";

            function i(i) {
                var o, s, r, a = this;
                i = i || {}, i.menu || t.error("menu is required"), this.isOpen = !1, this.isEmpty = !0, this.datasets = e.map(i.datasets, n), o = e.bind(this._onSuggestionClick, this), s = e.bind(this._onSuggestionMouseEnter, this), r = e.bind(this._onSuggestionMouseLeave, this), this.$menu = t(i.menu).on("click.tt", ".tt-suggestion", o).on("mouseenter.tt", ".tt-suggestion", s).on("mouseleave.tt", ".tt-suggestion", r), e.each(this.datasets, function(t) {
                    a.$menu.append(t.getRoot()), t.onSync("rendered", a._onRendered, a)
                })
            }

            function n(t) {
                return new m(t)
            }
            return e.mixin(i.prototype, d, {
                _onSuggestionClick: function(e) {
                    this.trigger("suggestionClicked", t(e.currentTarget))
                },
                _onSuggestionMouseEnter: function(e) {
                    this._removeCursor(), this._setCursor(t(e.currentTarget), !0)
                },
                _onSuggestionMouseLeave: function() {
                    this._removeCursor()
                },
                _onRendered: function() {
                    function t(t) {
                        return t.isEmpty()
                    }
                    this.isEmpty = e.every(this.datasets, t), this.isEmpty ? this._hide() : this.isOpen && this._show(), this.trigger("datasetRendered")
                },
                _hide: function() {
                    this.$menu.hide()
                },
                _show: function() {
                    this.$menu.css("display", "block")
                },
                _getSuggestions: function() {
                    return this.$menu.find(".tt-suggestion")
                },
                _getCursor: function() {
                    return this.$menu.find(".tt-cursor").first()
                },
                _setCursor: function(t, e) {
                    t.first().addClass("tt-cursor"), !e && this.trigger("cursorMoved")
                },
                _removeCursor: function() {
                    this._getCursor().removeClass("tt-cursor")
                },
                _moveCursor: function(t) {
                    var e, i, n, o;
                    if (this.isOpen) {
                        if (i = this._getCursor(), e = this._getSuggestions(), this._removeCursor(), n = e.index(i) + t, n = (n + 1) % (e.length + 1) - 1, -1 === n) return void this.trigger("cursorRemoved"); - 1 > n && (n = e.length - 1), this._setCursor(o = e.eq(n)), this._ensureVisible(o)
                    }
                },
                _ensureVisible: function(t) {
                    var e, i, n, o;
                    e = t.position().top, i = e + t.outerHeight(!0), n = this.$menu.scrollTop(), o = this.$menu.height() + parseInt(this.$menu.css("paddingTop"), 10) + parseInt(this.$menu.css("paddingBottom"), 10), 0 > e ? this.$menu.scrollTop(n + e) : i > o && this.$menu.scrollTop(n + (i - o))
                },
                close: function() {
                    this.isOpen && (this.isOpen = !1, this._removeCursor(), this._hide(), this.trigger("closed"))
                },
                open: function() {
                    this.isOpen || (this.isOpen = !0, !this.isEmpty && this._show(), this.trigger("opened"))
                },
                setLanguageDirection: function(t) {
                    this.$menu.css("ltr" === t ? c.ltr : c.rtl)
                },
                moveCursorUp: function() {
                    this._moveCursor(-1)
                },
                moveCursorDown: function() {
                    this._moveCursor(1)
                },
                getDatumForSuggestion: function(t) {
                    var e = null;
                    return t.length && (e = {
                        raw: m.extractDatum(t),
                        value: m.extractValue(t),
                        datasetName: m.extractDatasetName(t)
                    }), e
                },
                getDatumForCursor: function() {
                    return this.getDatumForSuggestion(this._getCursor().first())
                },
                getDatumForTopSuggestion: function() {
                    return this.getDatumForSuggestion(this._getSuggestions().first())
                },
                update: function(t) {
                    function i(e) {
                        e.update(t)
                    }
                    e.each(this.datasets, i)
                },
                empty: function() {
                    function t(t) {
                        t.clear()
                    }
                    e.each(this.datasets, t), this.isEmpty = !0
                },
                isVisible: function() {
                    return this.isOpen && !this.isEmpty
                },
                destroy: function() {
                    function t(t) {
                        t.destroy()
                    }
                    this.$menu.off(".tt"), this.$menu = null, e.each(this.datasets, t)
                }
            }), i
        }(),
        g = function() {
            "use strict";

            function i(i) {
                var o, s, r;
                i = i || {}, i.input || t.error("missing input"), this.isActivated = !1, this.autoselect = !!i.autoselect, this.minLength = e.isNumber(i.minLength) ? i.minLength : 1, this.$node = n(i.input, i.withHint), o = this.$node.find(".tt-dropdown-menu"), s = this.$node.find(".tt-input"), r = this.$node.find(".tt-hint"), s.on("blur.tt", function(t) {
                    var i, n, r;
                    i = document.activeElement, n = o.is(i), r = o.has(i).length > 0, e.isMsie() && (n || r) && (t.preventDefault(), t.stopImmediatePropagation(), e.defer(function() {
                        s.focus()
                    }))
                }), o.on("mousedown.tt", function(t) {
                    t.preventDefault()
                }), this.eventBus = i.eventBus || new h({
                    el: s
                }), this.dropdown = new v({
                    menu: o,
                    datasets: i.datasets
                }).onSync("suggestionClicked", this._onSuggestionClicked, this).onSync("cursorMoved", this._onCursorMoved, this).onSync("cursorRemoved", this._onCursorRemoved, this).onSync("opened", this._onOpened, this).onSync("closed", this._onClosed, this).onAsync("datasetRendered", this._onDatasetRendered, this), this.input = new f({
                    input: s,
                    hint: r
                }).onSync("focused", this._onFocused, this).onSync("blurred", this._onBlurred, this).onSync("enterKeyed", this._onEnterKeyed, this).onSync("tabKeyed", this._onTabKeyed, this).onSync("escKeyed", this._onEscKeyed, this).onSync("upKeyed", this._onUpKeyed, this).onSync("downKeyed", this._onDownKeyed, this).onSync("leftKeyed", this._onLeftKeyed, this).onSync("rightKeyed", this._onRightKeyed, this).onSync("queryChanged", this._onQueryChanged, this).onSync("whitespaceChanged", this._onWhitespaceChanged, this), this._setLanguageDirection()
            }

            function n(e, i) {
                var n, s, a, l;
                n = t(e), s = t(u.wrapper).css(c.wrapper), a = t(u.dropdown).css(c.dropdown), l = n.clone().css(c.hint).css(o(n)), l.val("").removeData().addClass("tt-hint").removeAttr("id name placeholder required").prop("readonly", !0).attr({
                    autocomplete: "off",
                    spellcheck: "false",
                    tabindex: -1
                }), n.data(r, {
                    dir: n.attr("dir"),
                    autocomplete: n.attr("autocomplete"),
                    spellcheck: n.attr("spellcheck"),
                    style: n.attr("style")
                }), n.addClass("tt-input").attr({
                    autocomplete: "off",
                    spellcheck: !1
                }).css(i ? c.input : c.inputWithNoHint);
                try {
                    !n.attr("dir") && n.attr("dir", "auto")
                } catch (h) {}
                return n.wrap(s).parent().prepend(i ? l : null).append(a)
            }

            function o(t) {
                return {
                    backgroundAttachment: t.css("background-attachment"),
                    backgroundClip: t.css("background-clip"),
                    backgroundColor: t.css("background-color"),
                    backgroundImage: t.css("background-image"),
                    backgroundOrigin: t.css("background-origin"),
                    backgroundPosition: t.css("background-position"),
                    backgroundRepeat: t.css("background-repeat"),
                    backgroundSize: t.css("background-size")
                }
            }

            function s(t) {
                var i = t.find(".tt-input");
                e.each(i.data(r), function(t, n) {
                    e.isUndefined(t) ? i.removeAttr(n) : i.attr(n, t)
                }), i.detach().removeData(r).removeClass("tt-input").insertAfter(t), t.remove()
            }
            var r = "ttAttrs";
            return e.mixin(i.prototype, {
                _onSuggestionClicked: function(t, e) {
                    var i;
                    (i = this.dropdown.getDatumForSuggestion(e)) && this._select(i)
                },
                _onCursorMoved: function() {
                    var t = this.dropdown.getDatumForCursor();
                    this.input.setInputValue(t.value, !0), this.eventBus.trigger("cursorchanged", t.raw, t.datasetName)
                },
                _onCursorRemoved: function() {
                    this.input.resetInputValue(), this._updateHint()
                },
                _onDatasetRendered: function() {
                    this._updateHint()
                },
                _onOpened: function() {
                    this._updateHint(), this.eventBus.trigger("opened")
                },
                _onClosed: function() {
                    this.input.clearHint(), this.eventBus.trigger("closed")
                },
                _onFocused: function() {
                    this.isActivated = !0, this.dropdown.open()
                },
                _onBlurred: function() {
                    this.isActivated = !1, this.dropdown.empty(), this.dropdown.close()
                },
                _onEnterKeyed: function(t, e) {
                    var i, n;
                    i = this.dropdown.getDatumForCursor(), n = this.dropdown.getDatumForTopSuggestion(), i ? (this._select(i), e.preventDefault()) : this.autoselect && n && (this._select(n), e.preventDefault())
                },
                _onTabKeyed: function(t, e) {
                    var i;
                    (i = this.dropdown.getDatumForCursor()) ? (this._select(i), e.preventDefault()) : this._autocomplete(!0)
                },
                _onEscKeyed: function() {
                    this.dropdown.close(), this.input.resetInputValue()
                },
                _onUpKeyed: function() {
                    var t = this.input.getQuery();
                    this.dropdown.isEmpty && t.length >= this.minLength ? this.dropdown.update(t) : this.dropdown.moveCursorUp(), this.dropdown.open()
                },
                _onDownKeyed: function() {
                    var t = this.input.getQuery();
                    this.dropdown.isEmpty && t.length >= this.minLength ? this.dropdown.update(t) : this.dropdown.moveCursorDown(), this.dropdown.open()
                },
                _onLeftKeyed: function() {
                    "rtl" === this.dir && this._autocomplete()
                },
                _onRightKeyed: function() {
                    "ltr" === this.dir && this._autocomplete()
                },
                _onQueryChanged: function(t, e) {
                    this.input.clearHintIfInvalid(), e.length >= this.minLength ? this.dropdown.update(e) : this.dropdown.empty(), this.dropdown.open(), this._setLanguageDirection()
                },
                _onWhitespaceChanged: function() {
                    this._updateHint(), this.dropdown.open()
                },
                _setLanguageDirection: function() {
                    var t;
                    this.dir !== (t = this.input.getLanguageDirection()) && (this.dir = t, this.$node.css("direction", t), this.dropdown.setLanguageDirection(t))
                },
                _updateHint: function() {
                    var t, i, n, o, s, r;
                    t = this.dropdown.getDatumForTopSuggestion(), t && this.dropdown.isVisible() && !this.input.hasOverflow() ? (i = this.input.getInputValue(), n = f.normalizeQuery(i), o = e.escapeRegExChars(n), s = new RegExp("^(?:" + o + ")(.+$)", "i"), r = s.exec(t.value), r ? this.input.setHint(i + r[1]) : this.input.clearHint()) : this.input.clearHint()
                },
                _autocomplete: function(t) {
                    var e, i, n, o;
                    e = this.input.getHint(), i = this.input.getQuery(), n = t || this.input.isCursorAtEnd(), e && i !== e && n && (o = this.dropdown.getDatumForTopSuggestion(), o && this.input.setInputValue(o.value), this.eventBus.trigger("autocompleted", o.raw, o.datasetName))
                },
                _select: function(t) {
                    this.input.setQuery(t.value), this.input.setInputValue(t.value, !0), this._setLanguageDirection(), this.eventBus.trigger("selected", t.raw, t.datasetName), this.dropdown.close(), e.defer(e.bind(this.dropdown.empty, this.dropdown))
                },
                open: function() {
                    this.dropdown.open()
                },
                close: function() {
                    this.dropdown.close()
                },
                setVal: function(t) {
                    t = e.toStr(t), this.isActivated ? this.input.setInputValue(t) : (this.input.setQuery(t), this.input.setInputValue(t, !0)), this._setLanguageDirection()
                },
                getVal: function() {
                    return this.input.getQuery()
                },
                destroy: function() {
                    this.input.destroy(), this.dropdown.destroy(), s(this.$node), this.$node = null
                }
            }), i
        }();
    ! function() {
        "use strict";
        var i, n, o;
        i = t.fn.typeahead, n = "ttTypeahead", o = {
            initialize: function(i, o) {
                function s() {
                    var s, r, a = t(this);
                    e.each(o, function(t) {
                        t.highlight = !!i.highlight
                    }), r = new g({
                        input: a,
                        eventBus: s = new h({
                            el: a
                        }),
                        withHint: e.isUndefined(i.hint) ? !0 : !!i.hint,
                        minLength: i.minLength,
                        autoselect: i.autoselect,
                        datasets: o
                    }), a.data(n, r)
                }
                return o = e.isArray(o) ? o : [].slice.call(arguments, 1), i = i || {}, this.each(s)
            },
            open: function() {
                function e() {
                    var e, i = t(this);
                    (e = i.data(n)) && e.open()
                }
                return this.each(e)
            },
            close: function() {
                function e() {
                    var e, i = t(this);
                    (e = i.data(n)) && e.close()
                }
                return this.each(e)
            },
            val: function(e) {
                function i() {
                    var i, o = t(this);
                    (i = o.data(n)) && i.setVal(e)
                }

                function o(t) {
                    var e, i;
                    return (e = t.data(n)) && (i = e.getVal()), i
                }
                return arguments.length ? this.each(i) : o(this.first())
            },
            destroy: function() {
                function e() {
                    var e, i = t(this);
                    (e = i.data(n)) && (e.destroy(), i.removeData(n))
                }
                return this.each(e)
            }
        }, t.fn.typeahead = function(e) {
            var i;
            return o[e] && "initialize" !== e ? (i = this.filter(function() {
                return !!t(this).data(n)
            }), o[e].apply(i, [].slice.call(arguments, 1))) : o.initialize.apply(this, arguments)
        }, t.fn.typeahead.noConflict = function() {
            return t.fn.typeahead = i, this
        }
    }()
}(window.jQuery),
function(t) {
    t.expr[":"].onScreen = function(e) {
        var i = t(window),
            n = i.scrollTop(),
            o = i.height(),
            s = n + o,
            r = t(e),
            a = r.offset().top,
            l = r.height(),
            u = a + l;
        return a >= n && s > a || u > n && s >= u || l > o && n >= a && u >= s
    }
}(jQuery),
function($) {
    $.fn.iframeTracker = function(t) {
        var e = this.get();
        if (null === t || t === !1) $.iframeTracker.untrack(e);
        else {
            if ("object" != typeof t) throw new Error("Wrong handler type (must be an object, or null|false to untrack)");
            $.iframeTracker.track(e, t)
        }
    }, $.iframeTracker = {
        focusRetriever: null,
        focusRetrieved: !1,
        handlersList: [],
        isIE8AndOlder: !1,
        init: function() {
            try {
                1 == $.browser.msie && $.browser.version < 9 && (this.isIE8AndOlder = !0)
            } catch (t) {
                try {
                    var e = navigator.userAgent.match(/(msie) ([\w.]+)/i);
                    e[2] < 9 && (this.isIE8AndOlder = !0)
                } catch (i) {}
            }
            if ($(window).focus(), $(window).blur(function(t) {
                    $.iframeTracker.windowLoseFocus(t)
                }), $("body").append('<div style="position:fixed; top:0; left:0; overflow:hidden;"><input style="position:absolute; left:-300px;" type="text" value="" id="focus_retriever" readonly="true" /></div>'), this.focusRetriever = $("#focus_retriever"), this.focusRetrieved = !1, $(document).mousemove(function(t) {
                    document.activeElement && "IFRAME" == document.activeElement.tagName && ($.iframeTracker.focusRetriever.focus(), $.iframeTracker.focusRetrieved = !0)
                }), this.isIE8AndOlder) {
                this.focusRetriever.blur(function(t) {
                    t.stopPropagation(), t.preventDefault(), $.iframeTracker.windowLoseFocus(t)
                }), $("body").click(function(t) {
                    $(window).focus()
                }), $("form").click(function(t) {
                    t.stopPropagation()
                });
                try {
                    $("body").on("click", "form", function(t) {
                        t.stopPropagation()
                    })
                } catch (t) {
                    console.log("[iframeTracker] Please update jQuery to 1.7 or newer. (exception: " + t.message + ")")
                }
            }
        },
        track: function(t, e) {
            e.target = t, $.iframeTracker.handlersList.push(e), $(t).bind("mouseover", {
                handler: e
            }, $.iframeTracker.mouseoverListener).bind("mouseout", {
                handler: e
            }, $.iframeTracker.mouseoutListener)
        },
        untrack: function(t) {
            if ("function" != typeof Array.prototype.filter) return void console.log("Your browser doesn't support Array filter, untrack disabled");
            $(t).each(function(t) {
                $(this).unbind("mouseover", $.iframeTracker.mouseoverListener).unbind("mouseout", $.iframeTracker.mouseoutListener)
            });
            var e = function(t) {
                return null === t ? !1 : !0
            };
            for (var i in this.handlersList) {
                for (var n in this.handlersList[i].target) - 1 !== $.inArray(this.handlersList[i].target[n], t) && (this.handlersList[i].target[n] = null);
                this.handlersList[i].target = this.handlersList[i].target.filter(e), 0 == this.handlersList[i].target.length && (this.handlersList[i] = null)
            }
            this.handlersList = this.handlersList.filter(e)
        },
        mouseoverListener: function(t) {
            t.data.handler.over = !0;
            try {
                t.data.handler.overCallback(this)
            } catch (e) {}
        },
        mouseoutListener: function(t) {
            t.data.handler.over = !1, $.iframeTracker.focusRetriever.focus();
            try {
                t.data.handler.outCallback(this)
            } catch (e) {}
        },
        windowLoseFocus: function(t) {
            for (var e in this.handlersList)
                if (1 == this.handlersList[e].over) try {
                    this.handlersList[e].blurCallback()
                } catch (i) {}
        }
    }, $(document).ready(function() {
        $.iframeTracker.init()
    })
}(jQuery), $(function() {
    var t = $("html"),
        e = $('form#sitesearch input[type="text"]'),
        i = $('form#sitesearch input[type="submit"]');
    i.prop("disabled", !0), e.keyup(function() {
        "" != $(this).val() ? i.prop("disabled", !1) : i.prop("disabled", !0)
    }), e.focusin(function() {
        t.hasClass("no-touch") && i.removeClass("animate-out").addClass("animate-in")
    }), e.focusout(function() {
        t.hasClass("no-touch") && i.removeClass("animate-in").addClass("animate-out")
    });
    var n = $(".lazy");
    n.show().lazyload({
        effect: "fadeIn",
        threshold: 100,
        failure_limit: 13
    });
    var o = $(".flexslider-controls");
    if (o.appendTo(".flex-viewport"), $(window).on("load", function() {
            $("body:not(#home) div.flexslider").flexslider({
                animationLoop: !0,
                smoothHeight: !1,
                animation: "slide",
                startAt: 0,
                slideshow: !0,
                slideshowSpeed: 7e3,
                animationSpeed: 600,
                initDelay: 0,
                pauseOnAction: !0,
                pauseOnHover: !1,
                touch: !0,
                video: !0,
                controlNav: !0,
                directionNav: !0,
                prevText: "Previous",
                nextText: "Next",
                controlsContainer: ".flexslider-controls",
                before: function(t) {
                    var e = t.slides.eq(t.animatingTo);
                    $(e).find("img").show().lazyload({})
                }
            })
        }), $("body#home").length) {
        var s = $("<b class='expand open'></b>"),
            r = $("li.tile > a");
        r.prepend(s), r.on("click focusin", function(t) {
            t.preventDefault(), $(this).next().find("img").lazyload({
                effect: "fadeIn",
                skip_invisible: !1
            }), $(".overlay").fadeOut(200), $(this).next().fadeIn(200), $(window).trigger("scroll")
        }), $(".overlay .expand").on("click focusin", function() {
            $(this).parent().parent().fadeOut(200)
        }), $("#newsticker").newsTicker({
            row_height: 110,
            max_rows: 3,
            speed: 400,
            direction: "up",
            duration: 6e3,
            autostart: 1,
            pauseOnHover: 1
        }), $(window).on("scroll", function(t) {
            $("#fundraising-progress .progress-bar:visible").filter(":onScreen").addClass("animate-in")
        }), $("#parttab").one("click focusin", function(t) {
            setTimeout(function() {
                $("#participation-progress .progress-bar").addClass("animate-in")
            }, 400)
        }), $(window).on("load", function() {
            var t = $("div.flexslider");
            t.flexslider({
                animationLoop: !0,
                smoothHeight: !1,
                animation: "slide",
                startAt: 0,
                slideshow: !0,
                slideshowSpeed: 7e3,
                animationSpeed: 600,
                initDelay: 0,
                pauseOnAction: !0,
                pauseOnHover: !1,
                touch: !0,
                video: !0,
                controlNav: !0,
                directionNav: !0,
                prevText: "Previous",
                nextText: "Next",
                controlsContainer: ".flexslider-controls",
                before: function(t) {
                    var e = t.slides.eq(t.animatingTo);
                    $(e).find("img").show().lazyload({}), $(e).find(".video-wrapper").length && ($(e).find(".video-wrapper").fadeOut(), $(".player")[0].contentWindow.postMessage('{"event":"command","func":"stopVideo","args":""}', "*"))
                }
            })
        })
    }
    if (!Modernizr.touch) {
        var a = $("a.tweet_line");
        a.on("click", function() {
            return newwindow = window.open($(this).attr("href"), "", "height=525,width=450"), window.focus && newwindow.focus(), !1
        })
    }
    if ($("body#explore").length) {
        var s = $("<b class='expand'></b>"),
            r = $("li.tile > a");
        r.prepend(s), r.on("click focusin", function(t) {
            t.preventDefault(), $(this).next().find("img").lazyload({
                effect: "fadeIn",
                skip_invisible: !1
            }), $(".overlay").fadeOut(200), $(this).next().fadeIn(200), $(window).trigger("scroll")
        }), $(".overlay .expand").on("click focusin", function() {
            $(this).parent().parent().fadeOut(200)
        })
    }
    if ($("body#priorities").length) {
        var l = $('form#prioritysearch input[type="text"]'),
            u = $('form#prioritysearch input[type="submit"]');
        u.prop("disabled", !0), l.keyup(function() {
            "" != $(this).val() ? u.prop("disabled", !1) : u.prop("disabled", !0)
        }), l.focusin(function() {
            t.hasClass("no-touch") && u.removeClass("animate-out").addClass("animate-in")
        }), l.focusout(function() {
            t.hasClass("no-touch") && u.removeClass("animate-in").addClass("animate-out")
        })
    }
    if ($("body#donor-recognition").length && $("#newsticker").newsTicker({
            row_height: 70,
            max_rows: 3,
            speed: 400,
            direction: "up",
            duration: 6e3,
            autostart: 1,
            pauseOnHover: 1
        }), $("body#feature_archive").length) {
        $("#feature_archivenav a").each(function() {
            ($(this).attr("href") == window.location.href || $(this).attr("href") == window.location.pathname) && $(this).addClass("on")
        });
        var l = $('form#featuresearch input[type="text"]'),
            u = $('form#featuresearch input[type="submit"]');
        u.prop("disabled", !0), l.keyup(function() {
            "" != $(this).val() ? u.prop("disabled", !1) : u.prop("disabled", !0)
        }), l.focusin(function() {
            t.hasClass("no-touch") && u.removeClass("animate-out").addClass("animate-in")
        }), l.focusout(function() {
            t.hasClass("no-touch") && u.removeClass("animate-in").addClass("animate-out")
        })
    }
});