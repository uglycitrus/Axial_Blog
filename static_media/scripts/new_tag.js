<tr><th><label for="id_form-0-name">Name:</label></th><td><input id="id_form-0-name" type="text" name="form-0-name" maxlength="50" /></td></tr> <tr><th><label for="id_form-1-name">Name:</label></th><td><input id="id_form-1-name" type="text" name="form-1-name" maxlength="50" /></td></tr> 

$(document).ready(
	function(){

		var num = $('.clonedInput').length;

		$('#btnAdd').click(function(){
			var num = $('.clonedInput').length;
			var newNum = new Number(num +1);
			var newElem = $('#id_form-'+num+'-name).clone().attr('id', '#id_form-'+newNum+'-name');
			newElem.children(':first').attr('name', 'battery_description'+newNum);
			newElem.find(':nth-child(2)').attr('name', 'type_number'+newNum);
			newElem.find(':nth-child(3)').attr('name', 'vkb_number'+newNum);
			newElem.find(':nth-child(5)').attr('name', 'quantity'+newNum);
			newElem.find(':nth-child(6)').attr('name', 'price'+newNum);
			$('input#id_rows').val(newNum);
			$('#input'+num).after(newElem);
			$('#btnDel').attr('disabled','');
			if (newNum == 10)
				$('#btnAdd').attr('disabled','disabled');
			}
		);

		$('#btnDel').click(function(){
			var num = $('.clonedInput').length;
			$('#input'+num).remove();
			$('#btnAdd').attr('disabled','');
			$('input#id_rows').val(num-1);
			if (num-1==1)
				$('#btnDel').attr('disabled','disabled');
			}
		);

	}
);

