(function ($) {
    'use strict'; $('.custom-content-rotator').each(function () { $(this).textRotator({ fadeSpeed: 500, pauseSpeed: 5000 }); }); var portfolioLoadMore = {
        pages: 0, currentPage: 1, $wrapper: $('#portfolioLoadMoreWrapper'), $btn: $('#portfolioLoadMore'), $btnWrapper: $('#portfolioLoadMoreBtnWrapper'), $loader: $('#portfolioLoadMoreLoader'), build: function () {
            var self = this
            self.pages = self.$wrapper.data('total-pages'); if (self.pages <= 1) { self.$btnWrapper.remove(); return; } else { self.$btn.on('click', function () { self.loadMore(); }); if (self.$btn.hasClass('btn-portfolio-infinite-scroll')) { theme.fn.intObs('#portfolioLoadMore', "$('#portfolioLoadMore').trigger('click');", { rootMargin: '0px 0px 0px 0px' }); } }
        }, loadMore: function () {
            var self = this, ajax_url = (self.$wrapper.data('ajax-url')) ? self.$wrapper.data('ajax-url') : 'ajax/portfolio-ajax-load-more-'; self.$btn.parent().find('.btn').hide(); self.$loader.addClass('portfolio-load-more-loader-showing').show(); $.ajax({
                url: ajax_url + (parseInt(self.currentPage) + 1) + '.html', complete: function (data) {
                    var $items = $(data.responseText); setTimeout(function () {
                        self.$wrapper.append($items); self.currentPage++; if (self.currentPage < self.pages) { self.$btn.parent().find('.btn').show().blur(); } else { self.$btnWrapper.remove(); }
                        $(function () {
                            $('[data-plugin-carousel]:not(.manual), .owl-carousel:not(.manual)').each(function () {
                                var $this = $(this), opts; var pluginOptions = theme.fn.getOptions($this.data('plugin-options')); if (pluginOptions)
                                    opts = pluginOptions; $this.themePluginCarousel(opts);
                            });
                        }); self.$loader.removeClass('portfolio-load-more-loader-showing').hide();
                    }, 1000);
                }
            });
        }
    }
    if ($('#portfolioLoadMoreWrapper').get(0)) { portfolioLoadMore.build(); }
    var portfolioLoadMore = {
        pages: 0, currentPage: 1, $wrapper: $('#portfolioLoadMoreWrapperBlog'), $btn: $('#portfolioLoadMoreBlog'), $btnWrapper: $('#portfolioLoadMoreBtnWrapperBlog'), $loader: $('#portfolioLoadMoreLoaderBlog'), build: function () {
            var self = this
            self.pages = self.$wrapper.data('total-pages'); if (self.pages <= 1) { self.$btnWrapper.remove(); return; } else { self.$btn.on('click', function () { self.loadMore(); }); if (self.$btn.hasClass('btn-portfolio-infinite-scroll')) { theme.fn.intObs('#portfolioLoadMoreBlog', "$('#portfolioLoadMoreBlog').trigger('click');", { rootMargin: '0px 0px 0px 0px' }); } }
        }, loadMore: function () {
            var self = this, ajax_url = (self.$wrapper.data('ajax-url')) ? self.$wrapper.data('ajax-url') : 'ajax/portfolio-ajax-load-more-'; self.$btn.parent().find('.btn').hide(); self.$loader.addClass('portfolio-load-more-loader-showing').show(); $.ajax({
                url: ajax_url + (parseInt(self.currentPage) + 1) + '.html', complete: function (data) {
                    var $items = $(data.responseText); setTimeout(function () {
                        self.$wrapper.append($items); self.currentPage++; if (self.currentPage < self.pages) { self.$btn.parent().find('.btn').show().blur(); } else { self.$btnWrapper.remove(); }
                        $(function () {
                            $('[data-plugin-carousel]:not(.manual), .owl-carousel:not(.manual)').each(function () {
                                var $this = $(this), opts; var pluginOptions = theme.fn.getOptions($this.data('plugin-options')); if (pluginOptions)
                                    opts = pluginOptions; $this.themePluginCarousel(opts);
                            });
                        }); self.$loader.removeClass('portfolio-load-more-loader-showing').hide();
                    }, 1000);
                }
            });
        }
    }
    if ($('#portfolioLoadMoreWrapperBlog').get(0)) { portfolioLoadMore.build(); }
    $('.simple-ajax-popup').magnificPopup({ type: 'ajax', callbacks: { open: function () { $('html').addClass('lightbox-opened'); }, close: function () { $('html').removeClass('lightbox-opened'); } } });
}).apply(this, [jQuery]);