$(document).ready(function() {
    $('#btnHide').click(function() {
        $('td:nth-child(2),th:nth-child(2)').toggle();
        <!--// if your table has header(th), use this
        //$('td:nth-child(2),th:nth-child(2)').hide(); -->
    });
    $('#btnHideVTL').click(function() {
        // $('td:nth-child(6),th:nth-child(6)').toggle();
        $('td:nth-child(7),th:nth-child(7)').toggle();
        $('td:nth-child(8),th:nth-child(8)').toggle();
        $('td:nth-child(9),th:nth-child(9)').toggle();
        $('td:nth-child(10),th:nth-child(10)').toggle();
        $('td:nth-child(11),th:nth-child(11)').toggle();
        $('td:nth-child(12),th:nth-child(12)').toggle();
        $('td:nth-child(13),th:nth-child(13)').toggle();
        $('td:nth-child(14),th:nth-child(14)').toggle();
        $('td:nth-child(15),th:nth-child(15)').toggle();
        $('td:nth-child(15),th:nth-child(16)').toggle();
    });
});
