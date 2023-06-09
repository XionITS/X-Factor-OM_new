
//SBOM 페이지
var aa = '../sbom_detail/?cpe='
var sbom_dataTable = function () {
    var dashboardpopupTable = $('#sbom_dataTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
        lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
        responsive: true,
        searching: true,
        ordering: false,
        serverSide: true,
        displayLength: false,
        ajax: {
            url: 'paging/',
            type: "POST",
            dataSrc: function (res) {
                var data = res.data.item;
                return data;
            }
        },
        columns: [
            {data: 'index', width: "5%"},
            {data: 'name', width: "15%"},
            {data: 'version', width: "10%"},
            {data: 'cpe', width: "50%"},
            {data: 'type', width: "10%"},
            {data: 'count', width: "10%"}
        ],
        columnDefs: [
            {targets: 0, width: "5%", className: 'text-center'},
            {
                targets: 1, width: "15%", className: '', render: function (data, type, row) {
                    return '<span style="color: #b6effb"; title="' + row.name + '" data-toggle="tooltip" onclick="openPopupWindow(\''+aa+row.cpe+'\', 1500, 600)">' + data + '<input type="hidden" name="cpe" value=row.cpe></a></span>'
                }
            },
            {
                targets: 2, width: "10%", className: '', render: function (data, type, row) {
                    return '<span title="' + row.version + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {targets: 3, width: "50%", style: 'text-center text-truncate', render: function (data, type, row) {
                    return '<span title="' + row.cpe + '" data-toggle="tooltip">' + data + '</span>'
                }},
            {targets: 4, width: "10%", className: 'text-center'},
            {targets: 5, width: "10%", className: 'text-center'},
        ],
        language: {
            "decimal": "",
            "info": "전체 _TOTAL_건",
            "infoEmpty": "데이터가 없습니다.",
            "emptyTable": "데이터가 없습니다.",
            "thousands": ",",
            "lengthMenu": "페이지당 _MENU_ 개씩 보기",
            "loadingRecords": "로딩 중입니다.",
            "processing": "",
            "zeroRecords": "검색 결과 없음",
            "paginate": {
                "first": "처음",
                "last": "끝",
                "next": "다음",
                "previous": "이전"
            },
            "search": "검색:",
            "infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
            "infoPostFix": "",
        },
        pagingType: 'numbers',

        drawCallback: function () {
            var current_page = dashboardpopupTable.page;
            var total_pages = dashboardpopupTable.page.info().pages;
            $('#nexts').remove();
            $('#after').remove();

            if (total_pages > 10) {
                $('<button type="button" class="btn" id="nexts">≫</button>')
                    .insertAfter('#sbom_dataTable_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="after">≪</button>')
                    .insertBefore('#sbom_dataTable_paginate .paginate_button:first');
            }
        }
    });

    $(document).on('click', '#nexts, #after', function() {
        var current_page = dashboardpopupTable.page();
        var total_pages = dashboardpopupTable.page.info().pages;
        if ($(this).attr('id') == 'nexts') {
                if (current_page + 10 < total_pages) {
                    dashboardpopupTable.page(current_page + 10).draw('page');
                } else {
                    dashboardpopupTable.page(total_pages - 1).draw('page');
                }
                } else {
                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
                }
    });
    $(document).ready(function() {
    var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
    });

};

function openPopupWindow(url, width, height){
    var left = (screen.width - width) /2;
    var top = (screen.height - height) /2;
    var windowFeatures = 'width=' + width + ',height=' + height + ', left=' + left + ', top'
    window.open(url, '_blank',windowFeatures)
    return false;
}

// var sbom_detail_dataTable = function () {
//     var dashboardpopupTable = $('#sbom_detail_dataTable').DataTable({
//         dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//         lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
//         responsive: true,
//         searching: true,
//         ordering: false,
//         serverSide: true,
//         displayLength: false,
//         ajax: {
//             url: 'paging/',
//             type: "GET",
//             dataSrc: function (res) {
//                 var data = res.data.item;
//                 return data;
//             }
//         },
//         columns: [
//             {data: 'index', width: "5%"},
//             {data: 'name', width: "15%"},
//             {data: 'version', width: "10%"},
//             {data: 'cpe', width: "50%"},
//             {data: 'type', width: "10%"},
//             {data: 'count', width: "10%"}
//         ],
//         columnDefs: [
//             {targets: 0, width: "5%", className: 'text-center'},
//             {
//                 targets: 1, width: "15%", className: '', render: function (data, type, row) {
//                     return '<span title="' + row.name + '" data-toggle="tooltip">' + data + '</span>'
//                 }
//             },
//             {
//                 targets: 2, width: "10%", className: '', render: function (data, type, row) {
//                     return '<span title="' + row.version + '" data-toggle="tooltip">' + data + '</span>'
//                 }
//             },
//             {targets: 3, width: "50%", style: 'text-center text-truncate', render: function (data, type, row) {
//                     return '<span title="' + row.cpe + '" data-toggle="tooltip">' + data + '</span>'
//                 }},
//             {targets: 4, width: "10%", className: 'text-center'},
//             {targets: 5, width: "10%", className: 'text-center'},
//         ],
//         language: {
//             "decimal": "",
//             "info": "전체 _TOTAL_건",
//             "infoEmpty": "데이터가 없습니다.",
//             "emptyTable": "데이터가 없습니다.",
//             "thousands": ",",
//             "lengthMenu": "페이지당 _MENU_ 개씩 보기",
//             "loadingRecords": "로딩 중입니다.",
//             "processing": "",
//             "zeroRecords": "검색 결과 없음",
//             "paginate": {
//                 "first": "처음",
//                 "last": "끝",
//                 "next": "다음",
//                 "previous": "이전"
//             },
//             "search": "검색:",
//             "infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//             "infoPostFix": "",
//         },
//         pagingType: 'numbers',
//
//         drawCallback: function () {
//             var current_page = dashboardpopupTable.page;
//             var total_pages = dashboardpopupTable.page.info().pages;
//             $('#nexts').remove();
//             $('#after').remove();
//
//             if (total_pages > 10) {
//                 $('<button type="button" class="btn" id="nexts">≫</button>')
//                     .insertAfter('#sbom_dataTable_paginate .paginate_button:last');
//                 $('<button type="button" class="btn" id="after">≪</button>')
//                     .insertBefore('#sbom_dataTable_paginate .paginate_button:first');
//             }
//         }
//     });
//
//     $(document).on('click', '#nexts, #after', function() {
//         var current_page = dashboardpopupTable.page();
//         var total_pages = dashboardpopupTable.page.info().pages;
//         if ($(this).attr('id') == 'nexts') {
//                 if (current_page + 10 < total_pages) {
//                     dashboardpopupTable.page(current_page + 10).draw('page');
//                 } else {
//                     dashboardpopupTable.page(total_pages - 1).draw('page');
//                 }
//                 } else {
//                     dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                 }
//     });
//     $(document).ready(function() {
//     var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//     $('head').append(customStyle);
//     });
//
// };


$(document).ready(function () {

    // if ($("#sbom_dataTable").length > 0) {

        sbom_dataTable();
        // sbom_detail_dataTable();
    // }
});

