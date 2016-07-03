module.exports = function () {
    console.log("Hello direktiva");
    return {
        restrict: 'E',
        scope: {
            info: '='
        },
        templateUrl: 'js/directives/movieDirective.html'
    };
};