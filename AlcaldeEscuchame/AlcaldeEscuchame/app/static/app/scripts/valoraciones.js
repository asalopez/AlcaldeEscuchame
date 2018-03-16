// Starrr plugin (https://github.com/dobtco/starrr)
var __slice = [].slice;

(function ($, window) {
    var Starrr;

    Starrr = (function () {
        Starrr.prototype.defaults = {
            rating: void 0,
            numStars: 5,
            change: function (e, value) { }
        };

        function Starrr($el, options) {
            var i, _, _ref,
                _this = this;

            this.options = $.extend({}, this.defaults, options);
            this.$el = $el;
            _ref = this.defaults;
            for (i in _ref) {
                _ = _ref[i];
                if (this.$el.data(i) != null) {
                    this.options[i] = this.$el.data(i);
                }
            }
            this.createStars();
            this.syncRating();
            this.$el.on('mouseover.starrr', 'span', function (e) {
                return _this.syncRating(_this.$el.find('span').index(e.currentTarget) + 1);
            });
            this.$el.on('mouseout.starrr', function () {
                return _this.syncRating();
            });
            this.$el.on('click.starrr', 'span', function (e) {
                return _this.setRating(_this.$el.find('span').index(e.currentTarget) + 1);
            });
            this.$el.on('starrr:change', this.options.change);
        }

        Starrr.prototype.createStars = function () {
            var _i, _ref, _results;

            _results = [];
            for (_i = 1, _ref = this.options.numStars; 1 <= _ref ? _i <= _ref : _i >= _ref; 1 <= _ref ? _i++ : _i--) {
                _results.push(this.$el.append("<span class='glyphicon .glyphicon-star-empty'></span>"));
            }
            return _results;
        };

        Starrr.prototype.setRating = function (rating) {
            if (this.options.rating === rating) {
                rating = void 0;
            }
            this.options.rating = rating;
            this.syncRating();
            return this.$el.trigger('starrr:change', rating);
        };

        Starrr.prototype.syncRating = function (rating) {
            var i, _i, _j, _ref;

            rating || (rating = this.options.rating);
            if (rating) {
                for (i = _i = 0, _ref = rating - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
                    this.$el.find('span').eq(i).removeClass('glyphicon-star-empty').addClass('glyphicon-star');
                }
            }
            if (rating && rating < 5) {
                for (i = _j = rating; rating <= 4 ? _j <= 4 : _j >= 4; i = rating <= 4 ? ++_j : --_j) {
                    this.$el.find('span').eq(i).removeClass('glyphicon-star').addClass('glyphicon-star-empty');
                }
            }
            if (!rating) {
                return this.$el.find('span').removeClass('glyphicon-star').addClass('glyphicon-star-empty');
            }
        };

        return Starrr;

    })();
    return $.fn.extend({
        starrr: function () {
            var args, option;

            option = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
            return this.each(function () {
                var data;

                data = $(this).data('star-rating');
                if (!data) {
                    $(this).data('star-rating', (data = new Starrr($(this), option)));
                }
                if (typeof option === 'string') {
                    return data[option].apply(data, args);
                }
            });
        }
    });
})(window.jQuery, window);

$(function () {
    return $(".starrr").starrr();
});

$(document).ready(function () {

    // Opciones posibles seg�n el n�mero de estrellas (0 a 5)
    var correspondence = ["", "La queja carece de importancia y no creo que sea de inter&#233;s general.", "La queja tiene trascendencia pero no creo que sea prioritaria.",
        "La queja es importante y puede resultar de inter&#233;s para la ciudadan&#237;a.", "La queja es muy importante y deber&#237;a ser atentida cuando antes.",
        "La queja es primordial y su resoluci&#243;n deber&#237;a ser prioritaria."];

    // Cuando se actua sobre las estrellas
    $('.ratable').on('starrr:change', function (e, value) {

        // Cambia los valores en el HTML para #count y #meaning
        $(this).closest('.evaluation').children('#count').html(value);
        $(this).closest('.evaluation').children('#meaning').html(" - " + correspondence[value]);

        // Div .indicators que contiene al formulario (bot�n de enviar)
        var target = $(this).closest('.evaluation').children('.indicators');
        // Actualiza el campo puntuaci�n del formulario y muestra el mismo.
        //document.getElementById("puntuacion").value = value;
        $('#puntuacion').val(value);
        target.css("display", "inline");

        if (!value || value <0) {
            target.css("display", "none");
            $(this).closest('.evaluation').children('#count').html(0);
            $(this).closest('.evaluation').children('#meaning').html(correspondence[0]);
            $('#puntuacion').val(null);
        }

        //target.css("color", "black");
        //target.children('.rateval').val(currentval);
        //target.children('#textwr').html(' ');


        //if (value < 3) {
        //    target.css("color", "red").show();
        //    target.children('#textwr').text('What can be improved?');
        //} else {
        //    if (value > 3) {
        //        target.css("color", "green").show();
        //        target.children('#textwr').html('What was done correctly?');
        //    } else {
        //        target.hide();
        //    }
        //}

    });
});

