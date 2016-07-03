module.exports = function () {
    return {
        restrict: 'E',
        scope: {
            info: '='
        },
        templateUrl: 'partials/movieDirective.html'
    };
};