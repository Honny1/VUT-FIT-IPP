ZIP_FILE_NAME=xrodak00
IS_IT_OK_SCRIPT=../is_it_ok.sh
IS_IT_OK_DIR=../is_it_ok_test_dir


.PHONY: pack is_it_ok is_it_ok_clean clean

pack: clean $(ZIP_FILE_NAME).zip

$(ZIP_FILE_NAME).zip:
	zip -D $(ZIP_FILE_NAME).zip parse_libs/*.php test_libs/*.php test_libs/*.html *.php interpretr_libs/*.py *.py *.md rozsireni

is_it_ok: clean $(ZIP_FILE_NAME).zip
	$(IS_IT_OK_SCRIPT) $(ZIP_FILE_NAME).zip $(IS_IT_OK_DIR)

is_it_ok_clean:
	rm -rf $(IS_IT_OK_DIR)

# Odstrani nepotrebne soubory
clean:
	rm -f $(ZIP_FILE_NAME).zip
