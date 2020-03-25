
myFunction();

// code here can use carName

function myFunction() {
    skillset = '';
} 

var i = 1;
function appendskill(){
    var _id ="'X"+i+"'"
    var skillname = ''
    if($('#skillname').val() != '' && !~skillset.indexOf($('#skillname').val())){
        skillname=$('#skillname').val();
        var skilldiv = '<div class="skilldiv"  id='+_id+'>\
                        <p style="display: inline;">'+skillname+'</p>\
                        <button class="close" type="button" onclick="removeskill('+_id+')" style="background:none;border:none;outline: inherit;position: relative;margin-top:1px">\
                            <i class="far fa-trash-alt" style="color:red;margin-left:15px;font-size:14px"></i>\
                        </button>\
                    </div>';
        $('#workform').append(skilldiv);
        $('#skillname').val('');
        i=i+1;
        skillset = skillset+skillname+',';
        skillname = ''
    }
}
function editskills(skl){
    var _id ="'X"+i+"'"
    var skilldiv = '<div class="skilldiv"  id='+_id+'>\
                        <p style="display: inline;">'+skl+'</p>\
                        <button class="close" type="button" onclick="removeskill('+_id+')" style="background:none;border:none;outline: inherit;position: relative;margin-top:1px">\
                            <i class="far fa-trash-alt" style="color:red;margin-left:15px;font-size:14px"></i>\
                        </button>\
                    </div>';
    $('#workform').append(skilldiv);
    i=i+1;
    skillset = skillset+skl+',';
    
}
function removeskill(skillid){
    var vl=$("#"+skillid+"").children("p").text();
    if(~skillset.indexOf(vl)){
        skillset =skillset.replace(vl+",","")
        $("#"+skillid+"").remove();
    }
}
/************************************/
$(document).ready(function(){
    var input = document.getElementById('skillname')
    input.addEventListener('keyup',function(e){
        e.preventDefault();
        if(e.keyCode == 13){
            appendskill();
        }
    });
    $('#crtform').keydown(function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });
    $('#crtform').on('submit',function(e){
        e.preventDefault();
        var self = $(this);//this form
        $('#skills').val(skillset);
        $("#crtform").off("submit");//need form submit event off.
        self.submit();//submit form
    });
});

